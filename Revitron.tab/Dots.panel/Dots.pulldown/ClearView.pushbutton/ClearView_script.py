import revitron
import dots

with revitron.Transaction():
	dots.removeExistingDots()
