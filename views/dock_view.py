import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update

class DocksView():

    def get(self, handler, pk):
        if pk != 0:
            sql = """
            SELECT
                d.id,
                d.location,
                d.capacity
            FROM Dock d
            WHERE d.id = ?
            """
            query_results = db_get_single(sql, pk)
            serialized_hauler = json.dumps(dict(query_results))

            return handler.response(serialized_hauler, status.SUCCESS)
        else:

            query_results = db_get_all("SELECT d.id, d.location, d.capacity FROM Dock d")
            haulers = [dict(row) for row in query_results]
            serialized_haulers = json.dumps(haulers)

            return handler.response(serialized_haulers, status.SUCCESS)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Dock WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.SUCCESS_NO_BODY)
        else:
            return handler.response("", status.NOT_FOUND)

    def update(self, handler, dock_data, pk):
        sql = """
        UPDATE Dock
        SET
            location = ?,
            capacity = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (dock_data['location'], dock_data['capacity'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.SUCCESS_NO_BODY)
        else:
            return handler.response("", status.NOT_FOUND)
