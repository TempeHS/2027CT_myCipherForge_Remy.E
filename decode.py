import engine

s = "hrkdbs"

if engine.decrypt(engine.encrypt(s)) == s:
    print(True)

else:
    print(False)
