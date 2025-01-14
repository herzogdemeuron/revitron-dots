import revitron
import json
import io
from os.path import dirname, join
from revitron import _
from pyrevit import revit, forms

DOT_FAMILY = 'RevitronDot'


def getConfig():
	config = revitron.DocumentConfigStorage().get('revitron.dots', dict())
	configFile = config.get('file', '')
	try:
		with io.open(configFile, encoding='utf-8') as f:
			return json.load(f)
	except:
		return False


def loadFamily():
	famSymId = None
	with revitron.Transaction():
		famSymId = findSymbolId()
		if not famSymId:
			path = join(
			    dirname(dirname(dirname(__file__))), 'rfa', '{}.rfa'.format(DOT_FAMILY)
			)
			revit.doc.LoadFamily(path)
			famSymId = findSymbolId()
	return famSymId


def findSymbolId():
	fltr = revitron.Filter().byCategory('DetailComponents')
	fltr = fltr.byStringEquals('Family Name', DOT_FAMILY).onlyTypes()
	try:
		return fltr.getElementIds()[0]
	except:
		return None


def removeExistingDots():
	fltr = revitron.Filter(revitron.ACTIVE_VIEW.Id).byCategory('DetailComponents')
	fltr = fltr.byStringEquals('Family Name', DOT_FAMILY).noTypes()
	elements = fltr.getElements()
	max_value = len(elements)
	counter = 0
	with forms.ProgressBar(
	    title='Deleting existing dots ... ({value} of {max_value})'
	) as pb:
		for dot in elements:
			_(dot).delete()
			counter += 1
			pb.update_progress(counter, max_value)


def createDots(element, colors, id, radius):
	try:
		view = revitron.ACTIVE_VIEW
		try:
			point = element.Location.Point
		except:
			point = element.GetTransform().Origin
		xyz = revitron.DB.XYZ
		grid = radius * 2.75
		n = len(colors)
		for m in range(n):
			offset = (m * grid) - ((n - 1) * grid * 0.5)
			_p = xyz(point.X + offset, point.Y, point.Z)
			dot = revitron.Create.familyInstance(id, _p, view=view)
			color = revitron.Color.fromHex(colors[m])
			ogs = revitron.DB.OverrideGraphicSettings()
			ogs.SetSurfaceForegroundPatternColor(color)
			view.SetElementOverrides(dot.Id, ogs)
			_(dot).set('Radius', radius)
	except Exception as e:
		print(e)


def filterElements(filters):
	fltr = revitron.Filter(revitron.ACTIVE_VIEW.Id)
	for f in filters:
		evaluator = getattr(revitron.Filter, f.get('rule'))
		fltr = evaluator(fltr, *f.get('args'))
	return fltr.noTypes().getElementIds()
