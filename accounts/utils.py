# accounts/utils.py
import random

# Fonction utilitaire pour générer un code OTP à 6 chiffres
def generate_otp():
    return str(random.randint(100000, 999999))