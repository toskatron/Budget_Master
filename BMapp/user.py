class User:
    def __init__(self, username, password, name=None, income=None, email=None):
        self.username = username
        self.password = password
        self.name = name
        self.income = income
        self.email = email

    @classmethod
    def get_user(cls, connection, username, password):
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                return cls(
                    name=result[1],
                    income=result[2],
                    username=result[3],  # Replace with the correct column name
                    email=result[4],  # Replace with the correct column name
                    password=result[5]  # Replace with the correct column name
                )
            else:
                return None
        except database.Error as e:
            print(f"Error fetching user data: {e}")
            return None