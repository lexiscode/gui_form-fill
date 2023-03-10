from tkinter import *
import sqlite3

root = Tk()
root.title("Learn to use SQLITE3")
root.maxsize(width=400, height=400)
root.minsize(width=400, height=400)
# root.geometry("400x400"), not necessary since there is now a root.min/maxsize() above
root.config(padx=10, pady=10)  # adds padding to the whole tk window

# Create a database or connect to one
conn = sqlite3.connect("contact_book.db")
# Create cursor
c = conn.cursor()
'''
# Create table
c.execute("""CREATE TABLE contact_details (
        first_name text,
        last_name text,
        address text,
        city text,
        state text,
        zipcode integer
        )""")
'''


# Submit to Database
def submit():
    # Create a database or connect to one
    submit_conn = sqlite3.connect("contact_book.db")
    # Create cursor
    submit_cursor = submit_conn.cursor()

    # Insert into table
    submit_cursor.execute("INSERT INTO contact_details VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
                          {
                              'f_name': f_name.get(),
                              'l_name': l_name.get(),
                              'address': address.get(),
                              'city': city.get(),
                              'state': state.get(),
                              'zipcode': zipcode.get()
                          })
    # Commit changes
    submit_conn.commit()
    # Close connection
    submit_conn.close()

    # Clear the textboxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


# Create Query function
def query():
    # Create a database or connect to one
    query_conn = sqlite3.connect("contact_book.db")
    # Create cursor
    query_cursor = query_conn.cursor()

    # Query the database
    query_cursor.execute("SELECT *, oid FROM contact_details")
    records = query_cursor.fetchall()
    # print(records), this prints all records in our console

    # Loop through results stored in the database
    print_records = ""
    for record in records:
        # print_records += str(record), this prints all records in form of a tuple
        # below prints specified contact details only
        print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) \
                         + " " + str(record[4]) + " " + str(record[5]) + " " + str(record[6]) + "\n"

    Label(root, text=print_records).grid(row=8, column=0, columnspan=2)

    # Commit changes
    query_conn.commit()
    # Close connection
    query_conn.close()


# Delete from the Database
def delete():
    # Create a database or connect to one
    delete_conn = sqlite3.connect("contact_book.db")
    # Create cursor
    delete_cursor = delete_conn.cursor()

    # Delete a record from the table
    delete_cursor.execute("DELETE from contact_details WHERE oid= " + select_entry.get())

    # Commit changes
    delete_conn.commit()
    # Close connection
    delete_conn.close()


# Save the Updated Database
def save():
    # Create a database or connect to one
    save_conn = sqlite3.connect("contact_book.db")
    # Create cursor
    save_cursor = save_conn.cursor()

    save_cursor.execute("""UPDATE contact_details SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode
    
        WHERE oid=:oid""",
                        {
                            'first': f_name_update.get(),
                            'last': l_name_update.get(),
                            'address': address_update.get(),
                            'city': city_update.get(),
                            'state': state_update.get(),
                            'zipcode': zipcode_update.get(),

                            'oid': select_entry.get()

                        })

    # Commit changes
    save_conn.commit()
    # Close connection
    save_conn.close()

    '''
    # Clear the textboxes/entries after the save button has been clicked
    f_name_update.delete(0, END)
    l_name_update.delete(0, END)
    address_update.delete(0, END)
    city_update.delete(0, END)
    state_update.delete(0, END)
    zipcode_update.delete(0, END)
    '''
    # the existence of this code below, makes the one above not necessary and commented out
    update_root.destroy()


# Update from the Database
def update():
    # this helps define the update_root variable in update_root.destroy() that's a bit above
    global update_root

    # Create a new tk window and object
    update_root = Tk()
    update_root.title("Update a Record")
    update_root.geometry("400x200")

    # Create global scope for textbox entries
    # this helps define the variables below in order for them to be able to be used above
    global f_name_update
    global l_name_update
    global address_update
    global city_update
    global state_update
    global zipcode_update

    # Create Labels and Entries (Textbox) # copied from first tk window with slight modifications
    Label(update_root, text="First Name").grid(row=0, column=0, pady=(10, 0))
    f_name_update = Entry(update_root, width=30)
    f_name_update.grid(row=0, column=1, padx=20, pady=(10, 0))

    Label(update_root, text="Last Name").grid(row=1, column=0)
    l_name_update = Entry(update_root, width=30)
    l_name_update.grid(row=1, column=1)

    Label(update_root, text="Address").grid(row=2, column=0)
    address_update = Entry(update_root, width=30)
    address_update.grid(row=2, column=1)

    Label(update_root, text="City").grid(row=3, column=0)
    city_update = Entry(update_root, width=30)
    city_update.grid(row=3, column=1)

    Label(update_root, text="State").grid(row=4, column=0)
    state_update = Entry(update_root, width=30)
    state_update.grid(row=4, column=1)

    Label(update_root, text="Zipcode").grid(row=5, column=0)
    zipcode_update = Entry(update_root, width=30)
    zipcode_update.grid(row=5, column=1)

    # Create a SAVE/UPDATE button
    save_update_btn = Button(update_root, text="Save/Update Record", command=save)
    save_update_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

    # Copied some codes from the query function is as shown below
    # Create a database or connect to one
    query_conn = sqlite3.connect("contact_book.db")
    # Create cursor
    query_cursor = query_conn.cursor()

    # Query the database
    query_cursor.execute("SELECT * FROM contact_details WHERE oid= " + select_entry.get())
    records = query_cursor.fetchall()
    # print(records), this prints the selected record in our console
    # To print the record into the fields of our new window, we do this
    for record in records:
        f_name_update.insert(0, record[0])
        l_name_update.insert(0, record[1])
        address_update.insert(0, record[2])
        city_update.insert(0, record[3])
        state_update.insert(0, record[4])
        zipcode_update.insert(0, record[5])


# Create Labels and Entries (Textbox)
# btw tho the pady=() below is not necessary since we already now have root.config() at the top
Label(root, text="First Name").grid(row=0, column=0, pady=(10, 0))
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))  # likewise in here

Label(root, text="Last Name").grid(row=1, column=0)
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

Label(root, text="Address").grid(row=2, column=0)
address = Entry(root, width=30)
address.grid(row=2, column=1)

Label(root, text="City").grid(row=3, column=0)
city = Entry(root, width=30)
city.grid(row=3, column=1)

Label(root, text="State").grid(row=4, column=0)
state = Entry(root, width=30)
state.grid(row=4, column=1)

Label(root, text="Zipcode").grid(row=5, column=0)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

Label(root, text="Select #ID").grid(row=9, column=0)
select_entry = Entry(root, width=30)  # initially this variable was delete_entry
select_entry.grid(row=9, column=1)

# Create SUBMIT button
submit_btn = Button(root, text="Add Record to Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=111)

# Create a QUERY button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create a DELETE button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create an UPDATE/EDIT button
update_btn = Button(root, text="Edit Record", command=update)
update_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

# Commit changes
conn.commit()
# Close connection
conn.close()

root.mainloop()
