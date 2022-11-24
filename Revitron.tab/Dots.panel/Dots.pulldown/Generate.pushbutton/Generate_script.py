import revitron
import dots
from revitron import _
from revitron.ui import SimpleWindow, SelectBox
from pyrevit import forms

symId = dots.loadFamily()
config = dots.getConfig()

if not config:
	forms.alert(
	    'Please first select a configuration file in the settings!', exitscript=True
	)

keys = config.keys()

window = SimpleWindow('Generate Dots', width=450, height=176)

SelectBox.create(window, 'Main', 'Setup', keys, keys[0])

window.show()
selected = None

if window.ok:
	selected = window.values['Setup']
	setup = config.get(selected)
	rules = setup.get('rules')
	radius = setup.get('radius', 1)

	elIdColorMap = dict()

	for rule in rules:
		color = rule.get('color')
		filters = rule.get('filters')
		for elId in dots.filterElements(filters):
			elId = elId.IntegerValue
			if elId not in elIdColorMap.keys():
				elIdColorMap[elId] = []
			elIdColorMap[elId].append(color)

	with revitron.Transaction():
		dots.removeExistingDots()
		max_value = len(elIdColorMap.keys())
		counter = 0
		with forms.ProgressBar(title='Creating Dots ... ({value} of {max_value})') as pb:
			for elId, colors in elIdColorMap.items():
				dots.createDots(_(elId).element, colors, symId, radius)
				counter += 1
				pb.update_progress(counter, max_value)
