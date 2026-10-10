"""soundtools：《節奏繞纏》期間累積的離線聲音工具，整理成可跨專案呼叫的套件。

模組
  io         讀寫、重取樣、淡入淡出、峰值與響度正規化
  varispeed  變速讀取、多聲部漂移、耦合、回歸、量化硬對齊
  tape       飽和、磁頭衰減、串音、tape echo、reverse delay、殘響、tape stop
  collage    時間軸疊放、交叉淡化、循環、電平器、最後鏈、paulstretch、顆粒雲
  analysis   樂句邊界、音節切分、stems 回對原檔

指令列：`soundtools --help`
"""
from . import io, varispeed, tape, collage, analysis  # noqa: F401

__version__ = "0.1.0"
