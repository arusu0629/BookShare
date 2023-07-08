# BookShare
Share book to instagram with Notion API and Instagram API

# Setup
1. Install pip
   ```bash
   // if not installed python
   $ brew install python

   // if installed already python
   $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   $ python get-pip.py

   $ python3 -m pip --version
   pip 23.1.2 from ~~~

   $ if needed
   alias=python3 -m pip
   ```
2. Install dependecies
   ```bash
   $ pip install -r requirements.txt
   ```

3. Update .env.example and Rename .env.example to .env
   ```python
   NOTION_API_KEY=
   NOTION_DATABASE_URL=
   NOTION_DATABASE_ID=

   INSTAGRAM_USERNAME=
   INSTAGRAM_PASSWORD=
   ```
