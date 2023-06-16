# <h1 align="center">Qustomate API</h1>

## <p>Register</p>
```
POST https://qustomate.et.r.appspot.com/auth/register
{
    "email":"sales2@gmail.com",
    "password":"sales002",
    "first_name":"Sales" ,
    "last_name": "2",
    "role":"sales",
    "company":"Toko Gawai Sejahtera"
}
```

## <p>Login</p>
```
POST https://qustomate.et.r.appspot.com/auth/login
{
            "email": "sales2@gmail.com",
            "password": "sales002"
}
```

## <p>Save Edit Management</p>
```
PUT https://qustomate.et.r.appspot.com/management/edit/sales-9a490dcf-8e21-4/chat-3cbc92d2-c7ec-4
{
        "alamat": "Bogor",
        "catatan": "Baju muslim 200",
        "kota": "Bogor",
        "name": "Sandi",
        "produk": "Baju Muslim",
        "revenue": 500000,
        "status": "selesai"
    }
```

## <p>Edit Management for placeholder</p>
```
GET https://qustomate.et.r.appspot.com/management/edit/sales-9a490dcf-8e21-4/chat-3cbc92d2-c7ec-4
```

## <p>List Management</p>
```
GET https://qustomate.et.r.appspot.com/management/list/sales-9a490dcf-8e21-4
```

## <p>Dashboard</p>
```
GET https://qustomate.et.r.appspot.com/dashboard/sales-9a490dcf-8e21-4
```

## <p>Message chat</p>
```
GET https://qustomate.et.r.appspot.com/message/chat/chat-3cbc92d2-c7ec-4
```

## <p>Contact</p>
```
GET https://qustomate.et.r.appspot.com/message/contact/sales-9a490dcf-8e21-4
```

## <p>Add Message</p>
```
POST https://qustomate.et.r.appspot.com/message/add
{
            "id_message": "010",
            "message_text": "pelayanan buruk",
            "recipientID": "Qustomate",
            "sender_id": "sender-02",
            "time_stamp":"2023-06-07T16:16:00"
}
```
