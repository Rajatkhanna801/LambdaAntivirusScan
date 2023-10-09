import pymysql


def create_cnx():
    try:
        conn = pymysql.connect(
            host='host',
            user='username',
            password='password',
            db='db_name',
            connect_timeout=15
        )
        print("Succesfully connected to RDS instance ...")
        return conn
    except pymysql.MySQLError as e:
        print("Error connecting to database exception=", e)
        raise e


def update_result(virus_scan_status, s3_file_path):
    """
        Method used to update results on Database.
    """
    print("Entered update_post function.")
    connection = create_cnx()
    cursor = connection.cursor()
    # The SQL query to update a cell
    sql = f"""
        UPDATE category_communitypost
        SET
            is_virus_scan_done=true,
            virus_scan_status='{virus_scan_status}'
        WHERE post_content_file='{s3_file_path}';
        """
    # Execute the query
    cursor.execute(sql)
    # Commit the changes
    connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Data successfully updated")
