from sage.all import *

# Public key matrix
pubkey = Matrix(ZZ, [
    [47, -77, -85],
    [-49, 78, 50],
    [57, -78, 99]
])

# Ciphertext vectors from enc.txt
ciphertexts = [
    vector([-981, 1395, -1668]),
    vector([6934, -10059, 4270]),
    vector([3871, -5475, 3976]),
    vector([4462, -7368, -8954]),
    vector([2794, -4413, -3461]),
    vector([5175, -7518, 3201]),
    vector([3102, -5051, -5457]),
    vector([7255, -10884, -266]),
    vector([5694, -8016, 6237]),
    vector([4160, -6038, 2582]),
    vector([4940, -7069, 3770]),
    vector([3185, -5158, -4939]),
    vector([7669, -11686, -2231]),
    vector([5601, -9013, -7971]),
    vector([5600, -8355, 575]),
    vector([1739, -2838, -3037]),
    vector([2572, -4120, -3788]),
    vector([8055, -11985, 1137]),
    vector([7088, -10247, 5141]),
    vector([8384, -12679, -1381]),
    vector([-785, 1095, -1841]),
    vector([4250, -6762, -5242]),
    vector([3716, -5364, 2126]),
    vector([5673, -7968, 6741]),
    vector([5877, -9190, -4803]),
    vector([5639, -8865, -5356]),
    vector([1980, -3230, -3366]),
    vector([6183, -9334, -1002]),
    vector([2575, -4068, -2828]),
    vector([7521, -11374, -1137]),
    vector([5639, -8551, -1501]),
    vector([4194, -6039, 3213]),
    vector([2072, -3025, 383]),
    vector([2444, -3699, -502]),
    vector([6313, -9653, -2447]),
    vector([4502, -7090, -4435]),
    vector([-421, 894, 2912]),
    vector([4667, -7142, -2266]),
    vector([4228, -6616, -3749]),
    vector([6258, -9719, -4407]),
    vector([6044, -9561, -6463]),
    vector([266, -423, -637]),
    vector([3849, -6223, -5988]),
    vector([5809, -9021, -4115]),
    vector([4794, -7128, 918]),
    vector([6340, -9442, 892]),
    vector([5322, -8614, -8334])
]

def fast_decrypt_with_known_patterns():
    """
    Fast decryption using known flag patterns
    """
    
    # HackTheBox flag patterns to try
    patterns = [
        "HTB{",  # Most likely HackTheBox format
        "HTB",   # Just the prefix
        "HACKTHEBOX{",
        "htb{",
        "hackthebox{",
        "CTF{",
        "FLAG{",
        "flag{",
        "{",
    ]
    
    pubkey_inv = pubkey.inverse()
    
    for pattern in patterns:
        print(f"Trying pattern: '{pattern}'")
        
        # Try this pattern at the beginning
        for start_pos in range(min(3, len(ciphertexts) - len(pattern) + 1)):
            try:
                # Use the pattern to find r
                pattern_chars = [ord(c) for c in pattern]
                
                # For each position in pattern, try to find consistent r
                potential_r = None
                all_consistent = True
                
                for i, char_val in enumerate(pattern_chars):
                    ct = ciphertexts[start_pos + i]
                    
                    # Try a few random combinations to find r
                    found_consistent_r = False
                    for rand1 in range(0, 101, 5):  # Try every 5th value for speed
                        for rand2 in range(0, 101, 5):
                            v = vector([char_val, rand1, rand2]) * pubkey
                            r_candidate = ct - v
                            
                            if potential_r is None:
                                potential_r = r_candidate
                                found_consistent_r = True
                                break
                            elif potential_r == r_candidate:
                                found_consistent_r = True
                                break
                        if found_consistent_r:
                            break
                    
                    if not found_consistent_r:
                        all_consistent = False
                        break
                
                if all_consistent and potential_r is not None:
                    print(f"Found potential r = {potential_r} for pattern '{pattern}' at position {start_pos}")
                    
                    # Try to decrypt with this r
                    flag = ""
                    valid_chars = 0
                    
                    for j, ct in enumerate(ciphertexts):
                        ct_no_r = ct - potential_r
                        pt_vec = ct_no_r * pubkey_inv
                        char_val = round(pt_vec[0])
                        
                        if 32 <= char_val <= 126:
                            flag += chr(char_val)
                            valid_chars += 1
                        else:
                            flag += "?"
                    
                    print(f"Decrypted: {flag}")
                    print(f"Valid chars: {valid_chars}/{len(ciphertexts)}")
                    
                    # Check if this looks like a valid flag
                    if (valid_chars > len(ciphertexts) * 0.8 and 
                        ('HTB' in flag or 'htb' in flag)):
                        print(f"SUCCESS! Flag: {flag}")
                        return flag
                        
            except Exception as e:
                print(f"Error with pattern {pattern}: {e}")
                continue
    
    return None

def htb_frequency_attack():
    """
    Use frequency analysis specifically for HTB flags
    """
    pubkey_inv = pubkey.inverse()
    
    # HTB flags typically start with 'H'
    char_val = ord('H')
    print(f"Trying first character: 'H' ({char_val})")
    
    # Sample random values to find r
    for rand1 in range(0, 101, 10):
        for rand2 in range(0, 101, 10):
            v = vector([char_val, rand1, rand2]) * pubkey
            r_candidate = ciphertexts[0] - v
            
            # Test this r on all ciphertexts
            flag = ""
            valid_count = 0
            
            for ct in ciphertexts:
                ct_no_r = ct - r_candidate
                pt_vec = ct_no_r * pubkey_inv
                char_val_test = round(pt_vec[0])
                
                if 32 <= char_val_test <= 126:
                    flag += chr(char_val_test)
                    valid_count += 1
                else:
                    flag += "?"
            
            print(f"Testing r={r_candidate}: {flag[:10]}... ({valid_count}/{len(ciphertexts)} valid)")

            if (valid_count > len(ciphertexts) * 0.8 and 
                flag.startswith('HTB')):
                print(f"SUCCESS! Flag: {flag}")
                return flag
    
    return None

def brute_force_htb():
    pubkey_inv = pubkey.inverse()
    print("Brute forcing for HTB{ pattern...")
    
    # HTB{ = [72, 84, 66, 123]
    pattern = "HTB{"
    pattern_chars = [ord(c) for c in pattern]
    
    # Try to find r using first 4 characters
    for rand1_0 in range(0, 101, 20):
        for rand2_0 in range(0, 101, 20):
            # Calculate r from first char 'H'
            v0 = vector([72, rand1_0, rand2_0]) * pubkey
            r_candidate = ciphertexts[0] - v0
            
            # Verify with remaining chars in HTB{
            valid_pattern = True
            for i in range(1, min(4, len(ciphertexts))):
                found_valid = False
                for rand1 in range(0, 101, 20):
                    for rand2 in range(0, 101, 20):
                        v = vector([pattern_chars[i], rand1, rand2]) * pubkey
                        if v + r_candidate == ciphertexts[i]:
                            found_valid = True
                            break
                    if found_valid:
                        break
                
                if not found_valid:
                    valid_pattern = False
                    break
            
            if valid_pattern:
                print(f"Found valid r for HTB: {r_candidate}")
                
                # Decrypt full flag
                flag = ""
                for ct in ciphertexts:
                    ct_no_r = ct - r_candidate
                    pt_vec = ct_no_r * pubkey_inv
                    char_val = round(pt_vec[0])
                    
                    if 32 <= char_val <= 126:
                        flag += chr(char_val)
                    else:
                        flag += "?"
                
                print(f"Flag: {flag}")
                if flag.startswith('HTB{') and flag.count('?') < len(flag) // 4:
                    return flag
    
    return None

# Main execution
print("=== HTB Quantum Safe Cryptography Solver ===")
print(f"Public key determinant: {pubkey.determinant()}")
print(f"Number of ciphertexts: {len(ciphertexts)}")

# Try HTB-specific methods first
result = fast_decrypt_with_known_patterns()
if result:
    print(f"\n🎉 Flag found: {result}")
else:
    print("\nPattern matching failed, trying HTB frequency analysis...")
    result = htb_frequency_attack()
    if result:
        print(f"\n🎉 Flag found: {result}")
    else:
        print("\nFrequency analysis failed, trying brute force HTB...")
        result = brute_force_htb()
        if result:
            print(f"\n🎉 Flag found: {result}")
        else:
            print("❌ All methods failed")