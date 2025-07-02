from flask import Flask
import mysql.connector
app = Flask(__name__)

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Pujitha15',
    database='mydatabase'
)

@app.route('/getTable',methods=['GET'])
def get_table():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM mytable")
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return {"data": rows}
if __name__ == '__main__':
    print("conn")
    app.run(debug=True)