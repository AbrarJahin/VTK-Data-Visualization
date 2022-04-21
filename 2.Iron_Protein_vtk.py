import vtk

dataLocation = "./data/ironProt.vtk"

dataReader = vtk.vtkStructuredPointsReader()
dataReader.SetFileName(dataLocation)
dataReader.Update()  # read data
width, height, depth = dataReader.GetOutput().GetDimensions()   #Read data dimention
sliderMinVal = 0
sliderMaxVal = 256

# computing a contour of an input data. 
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(dataReader.GetOutputPort())

isosurface.SetValue(0, (sliderMinVal + sliderMaxVal)/2)

duplicatePointsCleaner = vtk.vtkCleanPolyData()
duplicatePointsCleaner.SetInputConnection(isosurface.GetOutputPort())

normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(isosurface.GetOutputPort())
normals.SetFeatureAngle(45)

isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(normals.GetOutputPort())
isosurfaceMapper.SetColorModeToMapScalars()

figureOutline = vtk.vtkOutlineFilter()
figureOutline.SetInputConnection(dataReader.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(figureOutline.GetOutputPort())

renderer = vtk.vtkRenderer() 
renderer.SetBackground(0.65, 0.65, 0.65)
rendererWindow = vtk.vtkRenderWindow()
rendererWindow.SetSize(600, 600)
rendererWindow.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetSize(1600,1600)
iren.SetRenderWindow(rendererWindow)

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.8,0.3,0.7)
renderer.AddActor(outlineActor)

isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)
renderer.AddActor(isosurfaceActor)    

SliderRepres = vtk.vtkSliderRepresentation2D()
SliderRepres.SetMinimumValue(sliderMinVal)
SliderRepres.SetMaximumValue(sliderMaxVal)
SliderRepres.SetValue((sliderMinVal + sliderMaxVal) / 2)

SliderRepres.SetTitleText("Interactive Adjustable Slider")
SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.3, 0.05)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.7, 0.05)

SliderRepres.GetSelectedProperty().SetColor(1,0.5,0)

SliderRepres.SetTitleHeight(0.02)
SliderRepres.SetLabelHeight(0.02)

SliderRepres.SetSliderLength(0.02)
SliderRepres.SetSliderWidth(0.03)

SliderRepres.SetEndCapLength(0.01)
SliderRepres.SetEndCapWidth(0.03)

SliderRepres.SetTubeWidth(0.005)
SliderRepres.SetLabelFormat("%3.0lf")

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(iren)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)

def vtkSliderCallback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    print("Position ",pos)
    isosurface.SetValue(0, pos)

SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback)

rendererWindow.Render()

# initialize and start the interactor
iren.Initialize()
iren.Start()