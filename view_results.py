import sqlite3

def view_database(db_name):
    """Display all transactions from a database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    
    if not rows:
        print(f"No transactions in {db_name}")
        return
    
    print(f"\n{'='*80}")
    print(f"Database: {db_name}")
    print(f"{'='*80}")
    
    for row in rows:
        print(f"\nTransaction ID: {row[0]}")
        print(f"  Amount: ${row[1]}")
        print(f"  Time: {row[2]}")
        print(f"  Category: {row[3]}")
        print(f"  Distance from home: {row[4]} km")
        print(f"  Transactions in 1h: {row[5]}")
        if len(row) > 7:  # Fraud database has fraud_score
            print(f"  Fraud Score: {row[6]:.2f}")
            print(f"  Timestamp: {row[7]}")
        else:
            print(f"  Timestamp: {row[6]}")
    
    conn.close()
    print(f"\nTotal transactions: {len(rows)}")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("LEGITIMATE TRANSACTIONS")
    view_database('legitimate_transactions.db')
    
    print("\n\n" + "="*80)
    print("FRAUDULENT TRANSACTIONS")
    view_database('fraudulent_transactions.db')
    print("\n")
