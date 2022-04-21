import vtk

#==============================================================================
# 100^3 Samlping dataset of the Quadric function - Given in question
# x^2 + 0.5y^2+ 0.2z^2+ 0.1xz + 0.2x
#==============================================================================  

# create a data source from VTk Quadric
# F(x,y,z) = a0*x^2 + a1*y^2 + a2*z^2 + a3*x*y + a4*y*z + a5*x*z + a6*x + a7*y + a8*z + a9
# F(x,y,z) = 1*x^2 + 0.5*y^2 + 0.2*z^2 + 0*x*y + 0*y*z + 0.1*x*z + 0.2*x + 0*y + 0*z + 0

quadric = vtk.vtkQuadric()
quadric.SetCoefficients(1, 0.5, 0.2, 0, 0, 0.1, 0.2, 0, 0, 0)

dataSample = vtk.vtkSampleFunction()
dataSample.SetSampleDimensions(100, 100, 100)
dataSample.SetImplicitFunction(quadric)
sliderMinValue = 0.05
sliderMaxValue = 1.5

# computing a contour of an input data. 
isoSurface = vtk.vtkContourFilter()
isoSurface.SetInputConnection(dataSample.GetOutputPort())
isoSurface.SetValue(0,(sliderMinValue + sliderMaxValue)/2)

isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(isoSurface.GetOutputPort())
isosurfaceMapper.SetColorModeToMapScalars()

vtkOutline = vtk.vtkOutlineFilter()
vtkOutline.SetInputConnection(dataSample.GetOutputPort())
vtkOutlineMapper = vtk.vtkPolyDataMapper()
vtkOutlineMapper.SetInputConnection(vtkOutline.GetOutputPort())

renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderingWindow = vtk.vtkRenderWindow()
renderingWindow.SetSize(600, 600)
renderingWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetSize(1500,1500)
renderWindowInteractor.SetRenderWindow(renderingWindow)

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(vtkOutlineMapper)
outlineActor.GetProperty().SetColor(0.5,0.5,0.5)
renderer.AddActor(outlineActor)

isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)
renderer.AddActor(isosurfaceActor)

sliderRepresentation = vtk.vtkSliderRepresentation2D()
sliderRepresentation.SetMinimumValue(sliderMinValue)
sliderRepresentation.SetMaximumValue(sliderMaxValue)
sliderRepresentation.SetValue((sliderMinValue + sliderMaxValue)/2)
sliderRepresentation.SetTitleText("Interactive Adjustable Slider")
sliderRepresentation.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepresentation.GetPoint1Coordinate().SetValue(0.3, 0.05)
sliderRepresentation.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepresentation.GetPoint2Coordinate().SetValue(0.7, 0.05)

sliderRepresentation.SetSliderLength(0.02)
sliderRepresentation.SetSliderWidth(0.03)
sliderRepresentation.SetEndCapLength(0.01)
sliderRepresentation.SetEndCapWidth(0.03)
sliderRepresentation.SetTubeWidth(0.005)
sliderRepresentation.SetTitleHeight(0.02)
sliderRepresentation.SetLabelHeight(0.02)
sliderRepresentation.GetSelectedProperty().SetColor(1,0.5,0.5)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(renderWindowInteractor)
SliderWidget.SetRepresentation(sliderRepresentation)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)

def vtkSliderCallback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    isoSurface.SetValue(0, pos)

SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback)

renderingWindow.Render()

renderWindowInteractor.Initialize()
renderWindowInteractor.Start()