# HOW TO USE
0. Clone this repository
```bash
git clone https://github.com/susTuna/Seleksi-Sister.git
```
2. CD to Bagian-A
```bash
cd Bagian-A
```
3. Setup Venv
```bash
python -m venv venv
```
4. Activate Venv (Ubuntu)
```bash
source venv/bin/activate.sh
```
5. Install Deps
```bash
pip3 i -r requirements.txt
```
6. Create .env
```bash
PRIVATE_KEY = 'your private key'
PUBLIC_KEY = 'your public key'
NONCE = your nonce
BACKEND_URL = 'backendip:port'
TOTP_SECRET = 'your totp secret'
USERNAME = 'your username'
MAJOR = 'your major'
PASSWORD = 'your password'
```
7. Run each module
```bash
python -m test.%folder%.%filename% #no need .py

python -m test.keygen.keygen_test #generate pair (NO NEED IF U ALR HAVE KEY)

python -m test.submit.update_public_key #update your public key

python -m test.submit.submission_test -f path_to_file -p [1/2] #submit
```