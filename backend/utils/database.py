"""
Database utilities for storing inference logs
"""
from datetime import datetime
import sqlite3
from typing import Optional
import json


class InferenceLogger:
    def __init__(self, db_path="backend/inference_logs.db"):
        """
        Initialize inference logger with SQLite database
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inference_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_real BOOLEAN,
                confidence REAL,
                active_check_passed BOOLEAN,
                active_check_message TEXT,
                frame_data BLOB,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_inference(self, result: dict, frame_data: Optional[bytes] = None, metadata: Optional[dict] = None):
        """
        Log inference result to database
        Args:
            result: Detection result dictionary
            frame_data: Optional frame bytes
            metadata: Optional additional metadata
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO inference_logs 
            (is_real, confidence, active_check_passed, active_check_message, frame_data, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            result.get('is_real', False),
            result.get('confidence', 0.0),
            result.get('active_check_passed', False),
            result.get('active_check_message', ''),
            frame_data,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_logs(self, limit: int = 100):
        """
        Retrieve recent inference logs
        Args:
            limit: Maximum number of logs to retrieve
        Returns: List of log entries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM inference_logs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return logs
