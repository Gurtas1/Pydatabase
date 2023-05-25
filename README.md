# Python Database Interface
This is a comprehensive Python-based interface for a SQLite database, designed to facilitate a variety of interactions with the data. The application employs the `sqlite3` module for easier data manipulation, providing functionalities for addition, removal, sorting, and filtering of database items.

The User Interface (UI) is designed to be intuitive, presenting commands below the code for clear understanding of its operation. Data is initially read from .txt files if set by the user, and subsequently, the modified database can be saved back into these files. These preferences can be configured below the classes.

## Code overview
Class Structure
The main class, `Acomodation`, is implemented for managing the SQLite database. A nested class `Table` is used to create a GUI for interaction with the database using the Tkinter library.

## Usage
To instantiate the class, provide the database name along with file paths to two .txt files as arguments. For example:

```
database = Acomodation('hotels.db', True, 'table1.txt', 'table2.txt')
```

The `interactive_table()` method starts the Tkinter GUI for interaction with the database:
```
database.interactive_table() 
```

After interacting with the database, the `save_to_file()` method saves the database back into two .txt files:

```
database.save_to_file('table1.txt', 'table2.txt')
```
## Additional Features
The code supports the addition of new items to the database `add_item()`, removing existing items `remove_item()`, sorting `sort_table()` and filtering `filter()` of data.

*Please note that detailed information about these functionalities can be found in the comments within the code.*
