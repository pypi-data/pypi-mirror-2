from distutils.core import setup

setup(name='eyestudio',
    version='1.0.0',
    author="Gustav Larsson",
    author_email="slimgee@gmail.com",
    url="http://pypi.python.org/pypi/eyestudio/",
    description="Tool for evaluating and analysing eye movement classification algorithms.",
#    long_description="Tool for evaluating and analysing eye movement classification algorithms."
    packages=[
        'eyestudio', 
        'eyestudio.Analysis',
        'eyestudio.Engine',
        'eyestudio.Filtering',
        'eyestudio.Filters',
        'eyestudio.Metrics',
        'eyestudio.PyQt'],
        
    data_files=[('', ['eyestudio/Resources/icon.png'])],
        
)