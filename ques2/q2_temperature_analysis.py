# q2_temperature_analysis.py

import os
import csv
from statistics import pstdev  # population standard deviation

MONTHS = [
    "january","february","march","april","may","june",
    "july","august","september","october","november","december"
]

def month_to_season(m):     # Australian seasons
    if m == 12 or m == 1 or m == 2:
        return "Summer"
    elif m == 3 or m == 4 or m == 5:
        return "Autumn"
    elif m == 6 or m == 7 or m == 8:
        return "Winter"
    else:
        return "Spring"

def lowercase_index_map(header):
    m = {}
    i = 0
    while i < len(header):
        h = str(header[i]).strip().lower()
        m[h] = i
        i = i + 1
    return m

def parse_float_maybe(s):
    try:
        return float(str(s).strip())
    except:
        return None

def build_month_columns(idx_map):
    cols = []
    i = 0
    while i < 12:
        mon = MONTHS[i]
        if mon in idx_map:
            cols.append((i + 1, idx_map[mon]))
        i = i + 1
    return cols

def get_month_from_date(date_s):
    ds = str(date_s).strip()
    if "-" in ds:
        parts = ds.split("-")
        if len(parts) >= 2 and parts[1].isdigit():
            return int(parts[1])
    if "/" in ds:
        parts = ds.split("/")
        if len(parts) >= 2 and parts[1].isdigit():
            return int(parts[1])
    return None

def add_value(season_sum, season_cnt, station_min, station_max, station_vals,
              station_key, month_num, temp):
    sname = month_to_season(month_num)
    season_sum[sname] = season_sum[sname] + temp
    season_cnt[sname] = season_cnt[sname] + 1
    if station_key not in station_min:
        station_min[station_key] = temp
        station_max[station_key] = temp
        station_vals[station_key] = [temp]
    else:
        if temp < station_min[station_key]:
            station_min[station_key] = temp
        if temp > station_max[station_key]:
            station_max[station_key] = temp
        station_vals[station_key].append(temp)

def process_one_file(path, season_sum, season_cnt, station_min, station_max, station_vals):
    try:
        f = open(path, "r", encoding="utf-8-sig", newline="")
    except:
        return
    reader = csv.reader(f)

    header = next(reader, [])
    if header == []:
        f.close()
        return

    idx = lowercase_index_map(header)

    
    month_cols = build_month_columns(idx)

    
    long_station = None
    if "station" in idx:
        long_station = idx["station"]
    elif "station_id" in idx:
        long_station = idx["station_id"]

    long_date = None
    if "date" in idx:
        long_date = idx["date"]
    elif "day" in idx:
        long_date = idx["day"]
    elif "timestamp" in idx:
        long_date = idx["timestamp"]

    long_temp = None
    if "temperature" in idx:
        long_temp = idx["temperature"]
    elif "temp" in idx:
        long_temp = idx["temp"]
    elif "t" in idx:
        long_temp = idx["t"]

    
    name_idx = None
    if "station_name" in idx:
        name_idx = idx["station_name"]
    elif "station" in idx:
        name_idx = idx["station"]
    elif "name" in idx:
        name_idx = idx["name"]

    id_idx = None
    if "stn_id" in idx:
        id_idx = idx["stn_id"]
    elif "station_id" in idx:
        id_idx = idx["station_id"]
    elif "id" in idx:
        id_idx = idx["id"]

    wide_ok = (len(month_cols) > 0 and (name_idx is not None or id_idx is not None))
    long_ok = (long_station is not None and long_date is not None and long_temp is not None)

    if not wide_ok and not long_ok:
        f.close()
        return

    for row in reader:
        
        if wide_ok:
            name = ""
            sid = ""
            if name_idx is not None and name_idx < len(row):
                name = str(row[name_idx]).strip()
            if id_idx is not None and id_idx < len(row):
                sid = str(row[id_idx]).strip()
            if name == "" and sid == "":
                pass
            else:
                if sid != "":
                    station_key = name + " (" + sid + ")"
                else:
                    station_key = name

                k = 0
                while k < len(month_cols):
                    month_num, col = month_cols[k]
                    if col < len(row):
                        val = str(row[col]).strip()
                        if val != "":
                            low = val.lower()
                            if low != "nan" and low != "na" and low != "n/a":
                                temp = parse_float_maybe(val)
                                if temp is not None:
                                    add_value(season_sum, season_cnt, station_min, station_max, station_vals,
                                              station_key, month_num, temp)
                    k = k + 1
                if not long_ok:
                    continue

        if long_ok:
            if max(long_station, long_date, long_temp) >= len(row):
                continue
            station_key = str(row[long_station]).strip()
            date_s = str(row[long_date]).strip()
            temp_s = str(row[long_temp]).strip()
            if station_key == "" or date_s == "":
                continue
            if temp_s == "":
                continue
            l = temp_s.lower()
            if l == "nan" or l == "na" or l == "n/a":
                continue

            temp = parse_float_maybe(temp_s)
            if temp is None:
                continue

            mnum = get_month_from_date(date_s)
            if mnum is None or mnum < 1 or mnum > 12:
                continue

            add_value(season_sum, season_cnt, station_min, station_max, station_vals,
                      station_key, mnum, temp)

    f.close()

def write_average(season_sum, season_cnt, out_path):
    out = open(out_path, "w", encoding="utf-8")
    for s in ("Summer", "Autumn", "Winter", "Spring"):
        if season_cnt[s] > 0:
            avg = season_sum[s] / season_cnt[s]
            out.write(s + ": " + format(avg, ".1f") + "°C\n")
        else:
            out.write(s + ": No data\n")
    out.close()

def write_range(station_min, station_max, station_vals, out_path):
    out = open(out_path, "w", encoding="utf-8")
    if len(station_vals) == 0:
        out.write("No data\n")
        out.close()
        return

    ranges = {}
    max_range = None
    for st in station_vals:
        r = station_max[st] - station_min[st]
        ranges[st] = r
        if max_range is None or r > max_range:
            max_range = r

    for st in ranges:
        if abs(ranges[st] - max_range) < 1e-9:
            mx = station_max[st]
            mn = station_min[st]
            line = st + ": Range " + format(mx - mn, ".1f") + "°C (Max: " + format(mx, ".1f") + "°C, Min: " + format(mn, ".1f") + "°C)\n"
            out.write(line)
    out.close()

def write_stability(station_vals, out_path):
    out = open(out_path, "w", encoding="utf-8")
    if len(station_vals) == 0:
        out.write("No data\n")
        out.close()
        return

    stds = {}
    for st in station_vals:
        vals = station_vals[st]
        if len(vals) > 1:
            stds[st] = pstdev(vals)
        else:
            stds[st] = 0.0

    min_std = None
    max_std = None
    for st in stds:
        v = stds[st]
        if min_std is None or v < min_std:
            min_std = v
        if max_std is None or v > max_std:
            max_std = v

    for st in stds:
        v = stds[st]
        if abs(v - min_std) < 1e-9:
            out.write("Most Stable: " + st + ": StdDev " + format(v, ".1f") + "°C\n")
    for st in stds:
        v = stds[st]
        if abs(v - max_std) < 1e-9:
            out.write("Most Variable: " + st + ": StdDev " + format(v, ".1f") + "°C\n")
    out.close()

def main():
    season_sum = {"Summer": 0.0, "Autumn": 0.0, "Winter": 0.0, "Spring": 0.0}
    season_cnt = {"Summer": 0,   "Autumn": 0,   "Winter": 0,   "Spring": 0}
    station_min  = {}
    station_max  = {}
    station_vals = {}

    folder = "temperatures"
    if os.path.isdir(folder):
        files = os.listdir(folder)
        i = 0
        while i < len(files):
            fname = files[i]
            if fname.lower().endswith(".csv"):
                process_one_file(folder + "/" + fname, season_sum, season_cnt, station_min, station_max, station_vals)
            i = i + 1

    write_average(season_sum, season_cnt, "average_temp.txt")
    write_range(station_min, station_max, station_vals, "largest_temp_range_station.txt")
    write_stability(station_vals, "temperature_stability_stations.txt")

if __name__ == "__main__":
    main()
