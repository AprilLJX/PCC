import sqlite3

class userModel:

    def signup_model(self,phone,password):

        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()

        SQL = "SELECT userid from usertable where phone = '%s' " % phone
        user = c.execute(SQL)

        user = list(user)
        phone_exist = True if len(user) else False

        res = {}
        if phone_exist:
            res["status"] = '0'
        else:
            c.execute("INSERT INTO usertable(phone,password) VALUES (?,?)", (phone, password))
            conn.commit()
            res["status"] = '1'

        conn.close()

        return res