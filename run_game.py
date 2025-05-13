import subprocess
import os
DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(__file__)
print(DUONG_DAN_THU_MUC_HIEN_HANH)
subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "\\src\\menu.py"])