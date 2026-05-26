import pandas as pd
from app.database import engine


def load_dataframe_workout(sql_query):
    df = pd.read_sql(sql_query, engine)
    return df


def get_total_volume(df):
    total_vol = df["reps_performed"].sum()
    return total_vol


def get_volume_by_exercise(df):
    return df.groupby("name_of_exercise")["reps_performed"].sum()


def weekly_workout_volume(df):
    df = df.copy()
    df["week"] = pd.to_datetime(df["timestamp"]).dt.isocalendar().week
    result = df.groupby("week")["reps_performed"].sum().reset_index()
    return result


def get_best_workout(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    result = df.groupby("timestamp")["reps_performed"].sum().reset_index()
    return result
