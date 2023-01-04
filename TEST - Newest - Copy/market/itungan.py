import sqlite3
import functools

try:
    sqliteConnection = sqlite3.connect('C:/Users/Agnes/Downloads/Compressed/TEST - backup/market/market.db')
    cursor = sqliteConnection.cursor()

    # cursor.execute("select namaBarang, harga from dbarang")
    # barang = cursor.fetchall()z
    # print(barang)


    # cursor.execute("select totalStok from dbarang")
    # stock = cursor.fetchall()
    # print(stock)
    
    # cursor.execute("""select totalStok from dbarang where namaBarang = ?""", name,)
    # getstok = cursor.fetchall()
    # print(getstok)



# ************* untuk update *******************
    cursor.execute("select namaBarang from dbarang")
    name = cursor.fetchall()
    print(name)

    cursor.execute("select nama from trial")
    trialname = cursor.fetchall()
    print(trialname)

    # ini untuk nge looping sebanyak brang yang kedetect (saat ini hardcode/dummy)
    for i in range(len(trialname)):
        cursor.execute("""select totalStok from dbarang where namaBarang = ?""", trialname[i],)
        getstok = cursor.fetchall()
        print(getstok)

        # unutk gantu tuple jadi int
        res = functools.reduce(lambda sub, ele: sub * 10 + ele, getstok[0])
        updatestok = res - 1
        
        a = list(map(int, str(updatestok)))
        mystring =''.join(str(updateStok) for updateStok in a)
        # b = list(map(str, trialname))

        # print(str(mystring))
        # print(str(trialname[i]))


        cursor.execute("""update "dbarang" set "totalStok" = ? where "namaBarang" = ?""", (str(mystring), str(trialname[i])))
        sqliteConnection.commit()
# # ************* untuk update *******************

    # cursor.execute("select nama from trial")
    # transaksiTrialname = cursor.fetchall()
    # # print(transaksiTrialname)

    # # ini cuma coba" :
    # # cursor.execute("""select barangID, namaBarang, harga from dbarang where namaBarang = ?""", transaksiTrialname[i])
    # # utkHttransaksi = cursor.fetchall()
    # # print(utkHttransaksi)

    
    # test=0
    # # ini untuk nge looping sebanyak brang yang kedetect (saat ini hardcode/dummy)
    # for i in range(len(transaksiTrialname)):
    #     # print(trialname[i]) #utk cek ini bnr yg kluar trial name atau bkan
    #     cursor.execute("""select barangID, namaBarang, harga from dbarang where namaBarang = ?""", transaksiTrialname[i],)
    #     # ini untuk detail nya 
    #     # getstok = cursor.fetchall()
    #     # print(getstok)

        
    #     cursor.execute("""select namaBarang, harga from dbarang where namaBarang = ?""", transaksiTrialname[i],)
    #     getnamaharga = cursor.fetchall()
    #     print(getnamaharga)

    #     cursor.execute("""select harga from dbarang where namaBarang = ?""", transaksiTrialname[i])
    #     gettabelharga = cursor.fetchone()
        
    #     test = test + gettabelharga[0] 
    #     ini gmn cara supaya bisa masuk ke dlm sql nya 

    #     list(test[i])
    # print(type(test))
    
    # print(type(test))
    # res = list(map(int, str(test)))
    # print (test)

    # untuk update/ masukin total harga ke tabel header transaksi 
    # cursor.executemany("""insert into item (totalPayment)    (?);""",test)

    sqliteConnection.commit()


        
    


    



    # ini ngk bisa
    # updateStok = getstok - 1 
    # sqlquery = "update dbarang set totalStok = %s where trialname = %s "
    # params = (updateStok, name,)
    # cursor.execute(sqlquery, params)
    # sqliteConnection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
# finally:
#     if sqliteConnection:
#         sqliteConnection.close()
#         print("The SQLite connection is closed")
