SafeBite
Video Demo:  

SafeBite acts as a platform for stores to input their menus and customers may input their allergies and receive a list of foods they can and can’t eat. The program uses HTML, CSS, and JavaScript as the front end, SQLite as the database, and Python as the main program connecting the front and back end. Frameworks like BootStrape are used.

Online menus are often used rather than speaking to a server when eating out. As someone who has many allergies, dining is a hassle and unsafe. Embracing the technology revolution, I WISH I could just type in my allergies and be told immediately which items I can order and can’t.

There is no hardware requirement to fully run the application outside of an tablet or any device. There are no cost of building it.

Details:
SQL data storage - Using Sqlite3, I implemented tables called restaurants, which stores all restaurant info including description, id, name, and location; dishes, which includes the description, name, price, and id; ingredients, which includes id and name; and dish_ingredient, which links the ingredient id with dish id, indicating a relationship between the two tables.

Pull-down menu for the search bar - Using JS <li> and event listeners of the user clicks on search bar, pull down bar, and space previous of the other two, I’ve implemented a pull down search bar that will go through the SQL database and search for all restaurants to display according to the user input. E.g. if the user typed 's', it will show every restaurant that has 's' in their name. It is only shown visible when the user clicks on the search bar and turns invisible when the user clicks in spaces outside of the search bar and pull down bar.

Restaurants pages - Pages of index, restaurant registration, restaurant admin page, and login page are all built through html, css, and javascript. User login is stored in the restaurant data table and all passwords are encrypted as hash values. All admin pages are not accessible unless you login. The login status will be present even if you refresh the page.

Chatgpt API - Using ChatGPT API, I will ask chatgpt the prompt of: 

I will give you a list of sublists except for the first element of the list. I want you to immediately break this down into two parts, one with the allergy which is the first element of the list I provided you, this will be a list of allergies that is the ingredient someone is allergic to, call this ALLERGYNAME. For the second part, go to the second list of the list I provided, call this list the INGREDIENT LIST. Note that even if one of the sublists has multiple elements in them, still consider the whole sublist as one index. For example, if I gave you the list of [ ['nuts', ‘seafood’], [['chestnut', 'broccoli'], ['oil'], ['tuna'], ['fish'], ['peanut butter', 'beef'] , ['beans'], ['oil'], ['oil'], ['oil']]]. 'nuts' and ‘seafood’ are the ALLERGYNAME, ['chestnut', 'broccoli'] is considered as one subset, they have the index of 0. ['peanut butter', 'beef'] is the 4th sublist, therefore it will have an index of 3. The INGREDIENT LIST, contains a set of ingredients in the value of strings. I want you to output the index of all of the lists that have ingredients that are harmful to eat for someone who is allergic to the ALLERGYNAME. For example, someone won’t be able to eat ‘chestnut’, ‘tuna’, ‘fish’, and ‘peanut butter’ because they are harmful to people who are allergic to ‘seafood’ and ‘nuts’, therefore outputing: [0, 2, 3, 4] — a list of the indexes of the sublists that contains dangerous ingredients. For example, the output “0” indicates the sublist of ['chestnut', 'broccoli'] and the output “4” indicates the sublist of ['peanut butter', 'beef']. In the process of making the decision, try to dive into the causes of the allergies to assist you in making your decision, look for common foods that cause allergic reactions for the given allergy. Your output MUST BE ONLY ONE LIST, NO EXPLANATION NEEDED. If any general terms like 'animal products' are used, you are to ensure that everything that came from an animal, is also filtered out. These examples include: eggs, seafood, or any animal-derived products like cheese. 

Using the output of chatgpt, I will filter out any dishes that results in the output of yes and list them out in the menus page as unsafe. The menu uses Django to transfer SQL data to html elements. The 

Show ingredients from the admin portal - When the user logs in as the restaurant admin and checks the restaurant’s menu, it will show all the ingredients hidden in each dish, allowing them to visualize if any additional info needs to be imputed.

