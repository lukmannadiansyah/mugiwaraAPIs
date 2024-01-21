from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12677361'
app.config['MYSQL_PASSWORD'] = 'XHSflfPVnl'
app.config['MYSQL_DB'] = 'sql12677361'

mysql = MySQL(app)

def get_column_names(cursor):
    return [column[0] for column in cursor.description]

# Characters Endpoints
@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM characters")
        columns = get_column_names(cur)
        characters = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return jsonify(characters)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM characters WHERE id=%s", (character_id,))
        columns = get_column_names(cur)
        character = dict(zip(columns, cur.fetchone()))
        cur.close()

        if character:
            return jsonify(character)
        else:
            return jsonify({"message": "Character not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/characters', methods=['POST'])
def add_character():
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO characters (name, age, affiliation, position, devil_fruit, type) VALUES (%s, %s, %s, %s, %s, %s)",
                    (data['name'], data['age'], data['affiliation'], data['position'], data['devil_fruit'], data['type']))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Character added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE characters SET name=%s, age=%s, affiliation=%s, position=%s, devil_fruit=%s, type=%s WHERE id=%s",
                    (data['name'], data['age'], data['affiliation'], data['position'], data['devil_fruit'], data['type'], character_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Character updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM characters WHERE id=%s", (character_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Character deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Arcs Endpoints
@app.route('/arcs', methods=['GET'])
def get_arcs():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM arcs")
        columns = get_column_names(cur)
        arcs = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return jsonify(arcs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/arcs/<int:arc_id>', methods=['GET'])
def get_arc(arc_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM arcs WHERE id=%s", (arc_id,))
        columns = get_column_names(cur)
        arc = dict(zip(columns, cur.fetchone()))
        cur.close()

        if arc:
            return jsonify(arc)
        else:
            return jsonify({"message": "Arc not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arcs', methods=['POST'])
def add_arc():
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO arcs (arc, episodes, volumes, chapters) VALUES (%s, %s, %s, %s)",
                    (data['arc'], data['episodes'], data['volumes'], data['chapters']))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Arc added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arcs/<int:arc_id>', methods=['PUT'])
def update_arc(arc_id):
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE arcs SET arc=%s, episodes=%s, volumes=%s, chapters=%s WHERE id=%s",
                    (data['arc'], data['episodes'], data['volumes'], data['chapters'], arc_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Arc updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arcs/<int:arc_id>', methods=['DELETE'])
def delete_arc(arc_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM arcs WHERE id=%s", (arc_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Arc deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
