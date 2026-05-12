import os

print("repeater check")

f = open("mzz_torch.txt")
ftext = f.read()
f.close()

if "Done" == ftext:
    print("repeater: done and no need to repeat!\n")
else:
    print(f"repeater: progress only at '{ftext}', so repeating!")
    os.system("sbatch test.sh")
