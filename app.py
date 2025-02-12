from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import os
import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import LabelEncoder, StandardScaler
import uvicorn

app = FastAPI()

# Load the trained SVM model
model = load("svm_model.pkl")

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dataset Paths – Update paths if necessary
DATASETS = {
    "Attack-Free": os.path.join("extracted_feature", "CAN_attack_dataset1", "Attack_free_new.csv"),
    "DoS": os.path.join("extracted_feature", "CAN_attack_dataset1", "DoS_Attack_new.csv"),
    "Fuzzy": os.path.join("extracted_feature", "CAN_attack_dataset1", "Fuzzy_Attack_New.csv"),
    "Impersonation": os.path.join("extracted_feature", "CAN_attack_dataset1", "Impersonation_Attack_New.csv")
}

def preprocess_data(df):
    """
    Preprocess dataset:
    - Drops "Timestamp" column if present
    - Encodes categorical columns using LabelEncoder
    - Scales numerical features using StandardScaler
    """
    print("Preprocessing data...")

    df = df.drop(columns=["Timestamp"], errors="ignore")

    # Identify categorical columns (object type)
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Apply Label Encoding only to categorical columns
    label_encoder = LabelEncoder()
    for col in categorical_cols:
        df[col] = label_encoder.fit_transform(df[col])

    # Apply StandardScaler to numerical columns
    scaler = StandardScaler()
    df[df.columns] = scaler.fit_transform(df[df.columns])

    print("Preprocessing complete.")
    return df

# Serve the main HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

def majority_vote(arr):
    """Return the majority element from an array (as a Python int)"""
    unique, counts = np.unique(arr, return_counts=True)
    return int(unique[np.argmax(counts)])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive initial message with chosen attack type
        msg = await websocket.receive_text()
        req = json.loads(msg)
        attack_type = req.get("attack")

        if attack_type not in DATASETS:
            await websocket.send_text(json.dumps({"error": "Invalid attack type"}))
            return

        print(f"Loading dataset for: {attack_type}")
        df = pd.read_csv(DATASETS[attack_type])
        print(f"Dataset loaded successfully. Shape: {df.shape}")

        # Preprocess dataset
        df = preprocess_data(df)

        # --- Parameters ---
        rows_per_row_prediction = 15    # Each "row prediction" uses 15 data rows
        row_predictions_per_interval = 20  # 20 row predictions per 5-second interval
        interval_duration = 5  # seconds
        total_intervals = 12   # 12 intervals (1 min)

        pointer = 0
        interval_results = []

        # Process each 5-second interval:
        for interval in range(total_intervals):
            row_preds_for_interval = []  # Store 20 row predictions

            for _ in range(row_predictions_per_interval):
                if pointer + rows_per_row_prediction > len(df):
                    break

                # Get a batch of 15 rows (as one prediction input)
                batch = df.iloc[pointer:pointer + rows_per_row_prediction].values
                pointer += rows_per_row_prediction

                # Debug: Check batch shape
                print(f"Predicting on batch of shape: {batch.shape}")

                # Ensure batch has correct shape
                batch = batch.reshape(batch.shape[0], -1)

                preds = model.predict(batch)
                row_pred = majority_vote(preds)
                row_preds_for_interval.append(row_pred)

            if not row_preds_for_interval:
                break

            interval_majority = majority_vote(row_preds_for_interval)
            interval_results.append(interval_majority)

            await websocket.send_text(json.dumps({
                "prediction": interval_majority,
                "final": False
            }))

            await asyncio.sleep(interval_duration)

        if interval_results:
            overall_majority = majority_vote(interval_results)
        else:
            overall_majority = None

        await websocket.send_text(json.dumps({
            "prediction": overall_majority,
            "final": True
        }))

    except Exception as e:
        print(f"Error: {str(e)}")
        await websocket.send_text(json.dumps({"error": str(e)}))
    finally:
        await websocket.close()


@app.get("/attack", response_class=HTMLResponse)
async def serve_attack_page():
    with open("templates/attack_page.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


# Run the FastAPI app with increased timeout to prevent disconnections
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=300)
