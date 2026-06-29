from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tarun',
    maintainer_email='tarun@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = my_py_pkg.my_first_pynode:main",
            "my_pub = my_py_pkg.pub:main",
            "my_sub = my_py_pkg.sub:main",
            "sender = my_py_pkg.sender:main",
            "processor = my_py_pkg.processor:main",
            "add_two_ints_server = my_py_pkg.add_two_ints_server:main",
            "add_two_ints_client = my_py_pkg.add_two_ints_client:main",
            "hardware_status_pub = my_py_pkg.hardware_status_pub:main",
            "led_panel = my_py_pkg.led_panel:main",
            "battery = my_py_pkg.battery:main"
        ],
    },
)
