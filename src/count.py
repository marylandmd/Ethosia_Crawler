# from pymongo import MongoClient

# # Kết nối MongoDB
# client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/")
# db = client["mydatabase"]
# collection = db["jobs"]

# # Đếm tất cả documents trong collection
# count = collection.count_documents({})
# print("Số lượng documents:", count)


# MONGO_DBNAME=Workday
# MONGO_URI=mongodb+srv://nguyennduyylongg11:Hadong2003@cun.fg8jh.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority&appName=Cun

from pymongo import MongoClient

# Kết nối MongoDB bằng URI thực tế
MONGO_DBNAME = "Workday"
MONGO_URI = "mongodb+srv://nguyennduyylongg11:Hadong2003@cun.fg8jh.mongodb.net/" + MONGO_DBNAME + "?retryWrites=true&w=majority"

# Tạo client
client = MongoClient(MONGO_URI)

# Chọn database và collection
db = client[MONGO_DBNAME]
collection = db["workday_api"]   # đổi "jobs" thành tên collection bạn đã lưu

# Đếm tất cả documents
count = collection.count_documents({})
print("Số lượng documents trong collection jobs:", count)
