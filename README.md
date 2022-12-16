# DatabaseManagementSystem
Simple DBMS Demo

## Python implementation
- uses json library (part of Python)

## How to use
- in the terminal run the Main.py --> python3 Main.py
- This will prompt a input. Type in the DBMS commands.
- Copy paste of many commands work.

- The new release now allows for file parsing --> python3 Main.py file.txt

## Features
### 11.21.22
- Now includes join queries. The join type queries uses nested for loops to check and match rows.
    - NOTE: outer joins have additional processing to clean up the joined tables. This is necessary to control the no-match joins added into the final table.
### 12.25.22
- Transactions implementation. Transaction updates uses a .lock file to lock the table changed. The changes are saved into a cache until it is committed and permanently saved.