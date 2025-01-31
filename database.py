import firebase_admin
from firebase_admin import credentials , db

from datetime import datetime

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://speed-typing-test-shashi-singh-default-rtdb.firebaseio.com/"  # For Realtime Database 
})

ref = db.reference("test")
data = ref.get()

def checkUniqueUser(username): 
    for key,value in data.items():
        for names,entry in value.items():
            if entry==username:
                # print("found")
                return True
    return False

def initialiseNewUser(username,password):
    newValue = {
        "name":username,
        "password":password
    }
    ref.child(username).update(newValue)

def uploadCurrentData(username, wpm, accuracy):
    date = formatted_datetime
    newValue = {
        date: {
            "wpm": wpm,
            "accuracy": accuracy,
        },
    }
    try:
        if username != "Login":
            ref.child(username).child("history").push(newValue)
    except firebase_admin.exceptions.UnavailableError as e:
        print(f"Failed to upload data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def getHistory(username):
    newData = ref.child(username).child("history").get()
    output_list = []
    final_list = []
    temporary = []

    for a,b in newData.items():
        for date,pairValue in b.items():
            timestamp = date
            datetime_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            real_date = datetime_obj.date()
            real_time = datetime_obj.time()

            # print("Date: ",date)

            final_list.append(real_date)
            final_list.append(real_time)

            # print("finallist",final_list)

            for key,value in pairValue.items():
                # print(key,value)
                temporary.append(key)
                temporary.append(value)

            # print("pairValue",pairValue)
            # print("temporary",  temporary)
            final_list.append(temporary)

            temporary = []

        output_list.append(final_list)
        final_list = []

    # count = len(output_list)
    # print(count)
    # for i in output_list:
    #     print(i)

    return output_list



# def checking(username):
#     newData = ref.child(username).child("history").get()
#     count = len(newData)
#     print(count)

# getHistory("shashi")