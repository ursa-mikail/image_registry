import sqlite3
import csv
import hashlib
import hmac

# Initialize the database connection and create the table
def init_db():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contents TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            hmac TEXT NOT NULL,
            team TEXT NOT NULL,
            team_owner TEXT NOT NULL,
            status TEXT CHECK(status IN ('active', 'suspended', 'revoked')) NOT NULL DEFAULT 'active',
            status_signature TEXT,
            status_url TEXT
        )
    ''')
    conn.commit()
    return conn

# Create a new image record
def create_image(conn, name, contents, team, team_owner, secret_key, status="active", status_url=""):
    sha256_hash = hashlib.sha256(contents.encode()).hexdigest()
    hmac_hash = hmac.new(secret_key.encode(), contents.encode(), hashlib.sha256).hexdigest()
    data_to_sign = f"{name}{contents}{sha256_hash}{hmac_hash}{team}{team_owner}{status}{status_url}"
    status_signature = hmac.new(secret_key.encode(), data_to_sign.encode(), hashlib.sha256).hexdigest()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO image (name, contents, sha256, hmac, team, team_owner, status, status_signature, status_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, contents, sha256_hash, hmac_hash, team, team_owner, status, status_signature, status_url))
    conn.commit()

# Read an image record by name
def read_image(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM image WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        print("Image Record:", row)
    else:
        print("No record found.")

# Update an image record by name
def update_image(conn, name, new_contents, new_team, new_team_owner, secret_key, new_status="active", new_status_url=""):
    sha256_hash = hashlib.sha256(new_contents.encode()).hexdigest()
    hmac_hash = hmac.new(secret_key.encode(), new_contents.encode(), hashlib.sha256).hexdigest()
    data_to_sign = f"{name}{new_contents}{sha256_hash}{hmac_hash}{new_team}{new_team_owner}{new_status}{new_status_url}"
    new_status_signature = hmac.new(secret_key.encode(), data_to_sign.encode(), hashlib.sha256).hexdigest()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE image
        SET contents = ?, sha256 = ?, hmac = ?, team = ?, team_owner = ?, status = ?, status_signature = ?, status_url = ?
        WHERE name = ?
    ''', (new_contents, sha256_hash, hmac_hash, new_team, new_team_owner, new_status, new_status_signature, new_status_url, name))
    conn.commit()

# Delete an image record by name
def delete_image(conn, name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM image WHERE name = ?", (name,))
    conn.commit()

# Export SQL data to CSV
def export_to_csv(conn, file_path):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM image")
    rows = cursor.fetchall()
    with open(file_path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([desc[0] for desc in cursor.description])  # Write headers
        csvwriter.writerows(rows)

# Main execution
if __name__ == "__main__":
    conn = init_db()

    # Example usage
    secret_key = "supersecretkey"

    # Create example
    create_image(conn, "example_image", "example_data", "team_a", "owner_a", secret_key, "active", "")

    # Read example
    read_image(conn, "example_image")

    export_to_csv(conn, "images_export.csv")
    print("Data exported to images_export.csv")
    
    # Update example
    update_image(conn, "example_image", "new_data", "team_b", "owner_b", secret_key, "suspended", "https://example.com/cve-details")

    # Export to CSV example
    export_to_csv(conn, "images_export_new.csv")
    print("Data exported to images_export_new.csv")

    # Delete example
    delete_image(conn, "example_image")

    conn.close()


"""
Image Record: (2, 'example_image', 'example_data', 'd7f2db9e66297f3ac43a9ddcad1c9ec43c1becbba3b87dd1689ace47b9afed7c', '42558374b30a8eec6e7e5220a5a3bf4ee6921ed19bb2304dd4ce1604fd16ebbf', 'team_a', 'owner_a', 'active', 'b9c69ada4404dba178f64ce0bae66602567df9e826790a41abf2d7454e069542', '')
Data exported to images_export.csv
Data exported to images_export_new.csv
"""