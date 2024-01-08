from enigma import ePixmap, ePoint
from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_GUISKIN, resolveFilename, fileExists

def getLogoPath(logoType):
	def findLogo(logo):
		return (f := resolveFilename(SCOPE_GUISKIN, logo)) and fileExists(f) and f or ""
	if logoType == "model":
		if (f := findLogo("logos/boxlogo.svg")):
			return f
		elif (f := findLogo("logos/distrologo.svg")):
			return f
	elif logoType == "brand":
		return findLogo("logos/brandlogo.svg")
	elif logoType == "distro":
		return findLogo("logos/distrologo.svg")
	return ""

def getDefaultLogo(logoType, width, height):
		if logoType == "model":
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo.svg")
		elif logoType == "brand":
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo_small.svg")
		else:
			defaultLogoPath = resolveFilename(SCOPE_GUISKIN, "skinlogo.svg")

		return detectAndFitPix(defaultLogoPath, width=width, height=height)

def detectAndFitPix(path, width, height):
	is_svg = path and path.endswith(".svg")
	if path:
		px_orig = LoadPixmap(path) #load pixmap so to detect the aspect ratio due to the fact smart fit is not implemented in c++
		px_orig_size = px_orig.size()
		isFitByWidth = px_orig_size.width() > px_orig_size.height()
		isFitByHeight = px_orig_size.width() < px_orig_size.height()
		return LoadPixmap(path, width=0 if is_svg and isFitByWidth else width, height=0 if is_svg and isFitByHeight else height)
	return None

def setLogo(px, logoType, width, height):
	logoPath = getLogoPath(logoType)
	pix = detectAndFitPix(logoPath, width=width, height=height)
	if pix:
		px.setPixmap(pix)
		centerLogo(px, pix, width, height)
	else:
		defaultLogo = getDefaultLogo(logoType, width, height)
		if defaultLogo:
			px.setPixmap(defaultLogo)
			centerLogo(px, defaultLogo, width, height)

def centerLogo(px, px_scaled, width, height):
	px_size = px_scaled.size()
	px_pos = px.position()
	x = 0
	y = 0
	if px_size.width() < width:
		x = (width - px_size.width()) // 2
	
	if px_size.height() < height:
		y = (height - px_size.height()) // 2
		
	px.move(ePoint(px_pos.x() + x, px_pos.y() + y))
	px.resize(px_size)

class BoxLogo(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.logoType = "model"
		
	GUI_WIDGET = ePixmap

	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == "logoType":
				self.logoType = value
				attribs.remove((attrib, value))
				break
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def changed(self, what):
		pass
				
	def onShow(self):
		if self.instance:
			setLogo(self.instance, self.logoType, self.instance.size().width(), self.instance.size().height())