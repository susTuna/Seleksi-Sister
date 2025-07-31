# HOW TO USE
**1. Clone this repository**
```bash
git clone https://github.com/susTuna/Seleksi-Sister.git
```
**2. CD to Bagian-A**
```bash
cd Bagian-A
```
**3. Setup Venv**
```bash
python -m venv venv
```
**4. Activate Venv (Ubuntu)**
```bash
source venv/bin/activate.sh
```
**5. Install Deps**
```bash
pip3 i -r requirements.txt
```
**6. Generate keys**
```bash
python -m test.keygen.keygen_test
```
**7. Create .env**
```bash
PRIVATE_KEY = 'your private key'
PUBLIC_KEY = 'your public key'
NONCE = your nonce # will be generated later
BACKEND_URL = 'backendip:port'
TOTP_SECRET = 'your totp secret' #will be found after activating account
USERNAME = 'your username'
MAJOR = 'your major'
PASSWORD = 'your password'
```
**8. Generate Nonce and Activate Account**
```bash
python -m test.nonce.nonce_test #copy result to .env
python -m test.activate.activate
```
**9. Submit**
```bash
python -m test.submit.submission_test -f path_to_file -p [1/2] #submit
```
**10. Optional***
```bash
python -m test.submit.update_public_key #update your public key if needed
```