from . import NumberNormalization_ZN
from . import NumberNormalization_EN

# 合并字典，保留两个字典的内容
NODE_CLASS_MAPPINGS = {**NumberNormalization_ZN.NODE_CLASS_MAPPINGS, **NumberNormalization_EN.NODE_CLASS_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {**NumberNormalization_ZN.NODE_DISPLAY_NAME_MAPPINGS, **NumberNormalization_EN.NODE_DISPLAY_NAME_MAPPINGS}
