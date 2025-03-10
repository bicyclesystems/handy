![handy](./images/handy.svg)

## intro

handy is a revolutionary tool that turns your everyday spaces into an intuitive, ergonomic platform for interacting seamlessly with your computer. instead of relying on a traditional desktop mouse or trackpad, it leverages advanced technology to convert your hand gestures into digital commands, redefining the way you engage with your digital world.
handy was developed with the vision of making computers more accessible, intuitive, and enjoyable. it aims to provide a more natural and ergonomic alternative to traditional input devices.

### features

- advanced gesture recognition technology
- adaptable to different surfaces
- open-source api for customization and integration
- versatile for various user needs, from casual browsing to professional applications

### users

handy is designed for creative people such as:

- designers
- musicians
- casual users and anyone looking for a more natural and ergonomic alternative to the traditional mouse

### system

handy's system consists of hardware and software components working together to capture hand movements and translate them into digital commands. the core of this system is the advanced algorithms that adapt to different surfaces for consistent performance.

### app

the handy app provides a simple, intuitive user interface to configure settings. it includes:

- management of gesture presets
- device firmware updates
- status bar indicator for motion capturing states
- gesture customization tools

supported platforms: macos and windows

### framework

the handy framework is an open-source platform that allows users to:

- create, customize, and share gestures
- contribute to the development of new gestures
- expand the range of supported gestures
- improve the overall user experience through community collaboration

### hemi

hemi is a small, hemisphere-shaped device that captures movement with high performance and ergonomics. it enhances the user experience, elevating gesture control technology from casual to professional needs.

key features:

- compact, high-resolution camera with a wide field of view
- infrared or depth-sensing capabilities for better performance and adaptability
- sleek, modern design that blends well with various desk setups

## app

### requirements

(specific hardware requirements, software dependencies, and os compatibility would be listed here)

### install

- download the handy application installer for your operating system (macos or windows).
- run the installer and follow the on-screen instructions.
- once installed, launch the handy application.

### setup

- open the handy application.
- follow the on-screen calibration process.
- adjust sensitivity settings to your preference.
- choose a default gesture preset or create a custom one.
    
    (information on available preset categories and how to activate/switch presets would be provided here)
    

### gestures

handy includes a virtual trackpad driver that interfaces with the operating system's trackpad apis. this driver is responsible for passing the translated gesture events to the operating system. it implements a mechanism to map the recognized gestures into trackpad events, such as taps, swipes, and pinches, compatible with the trackpad apis of macos and windows.

| gesture name | description |
| --- | --- |
| move | finger touch and moves. |
| single tap | a quick tap with one finger on the table surface, equivalent to a left-click on a traditional mouse. |
| double tap | two quick taps with one finger on the table surface, used to open files or applications, and access context menus. |
| two-finger tap | a simultaneous tap with two fingers on the table surface, equivalent to a right-click on a traditional mouse. |
| tap and hold | tapping and holding one finger on the table surface, equivalent to clicking and holding the left mouse button. |
| two-finger scroll | placing two fingers on the table surface and moving them up or down to scroll vertically or left and right to scroll horizontally. |
| pinch-to-zoom | placing two fingers on the table surface and moving them closer together or further apart to zoom in or out of content. |
| rotate | placing two fingers on the table surface and moving them in a circular motion to rotate objects or content. |
| three-finger swipe | swiping three fingers across the table surface to switch between applications, desktops, or browser tabs. |
| four-finger swipe | swiping four fingers across the table surface to show the desktop or reveal all open windows (similar to exposé or task view on macos and windows). |
| keyboard events |  |

### ui

(detailed description of the app's dashboard, menu structure, and customization options would be provided here)

### basics

- starting/stopping gesture recognition
- switching between gesture sets
- viewing active gestures

### settings

the handy app includes options for:

- sensitivity adjustments
- gesture customization
- managing gesture presets
- updating device firmware
- integration with other software

### calibration

(step-by-step calibration guide and information on when to recalibrate would be included here)

### updates

(instructions for checking for updates, the update process, and rollback procedures would be detailed here)

### status

the handy app includes a small desktop indicator application that displays the current status of the motion capturing:

- active
- error
- processing/input
- standby

this indicator replaces the need for a physical led indicator on the device itself. handy automatically looks for active software that works with its active gestures. if it finds any, it connects the gestures to that software.

## framework

### sensors

- gesture recognition: advanced computer vision algorithms
- motion tracking: 6-axis motion tracking (accelerometer + gyroscope)
- surface adaptation: ai-driven surface recognition for consistent performance

### custom gestures

(instructions for the gesture recording process, defining gesture parameters, and testing/refining gestures would be provided here)

### best practices

(tips for optimal lighting, hand positioning, and gesture complexity would be detailed here)

### troubleshooting

(common recognition errors, calibration tips, and guidelines for when to retrain gestures would be listed here)

### presets

(information on authoring tools and the validation process for gesture presets would be provided here)

(workflow for creating presets, adding/removing gestures, and setting default presets would be detailed here)

### gestures.handy

the gestures.handy file uses a json format. here's an example structure:

```json
{
  "meta": {
    "version": "1.0",
    "name": "trackpad gesture set"
  },
  "models": {
    "handrecognition": "default_model",
    "additionalmodels": []
  },
  "gestures": {
    "primitive": [
      {
        "name": "tap",
        "code": "function tap() { /* code here */ }"
      },
      {
        "name": "scroll",
        "code": "function scroll() { /* code here */ }"
      }
      // more primitive gestures
    ],
    "custom": [
      {
        "name": "twofingertap",
        "code": "function twofingertap() { /* code here */ }"
      }
      // more custom gestures
    ]
  },
  "mapping": null // no need for mapping here as it's handled by the sdk on the software side
}
```

### mapping

(available system actions and instructions for creating basic mappings would be listed here)

### custom mapping

(guidelines for defining custom actions and using macros/scripts would be provided here)

### context

(instructions for setting up application-specific gestures and using gestures based on system state would be detailed here)

### advanced

(information on chaining multiple actions, using modifiers with gestures, and creating adaptive gesture responses would be provided here)

### versions

(details on the versioning scheme and backward compatibility considerations would be included here)

## hemi

hemi, the sensor that powers handy, captures the magic of your gestures. this sleek, half-dome device acts as handy's eyes, sending ultra-wide 180-degree black-and-white images at lightning speed. with its keen vision, hemi enables handy to interpret your movements into computer commands with instantaneous responsiveness, bringing your gestures to life on screen.

the device has a half-spherical shape with a flat base, allowing it to sit stably on the table surface. this design provides an elegant, modern appearance while ensuring a wide field of view for capturing gestures.

### specs

- dimensions:
    - height: 2.5 cm
    - width: 5 cm
    - depth: 5 cm
- weight: 100 grams (estimated, to be confirmed)
- design: half-spherical shape with a flat base
- materials: high-quality plastic and metal for durability and heat dissipation

### camera

- type: high-resolution depth-sensing camera
- resolution: 1080p (1920x1080 pixels)
- frame rate: 120 fps for ultra-smooth motion capture
- field of view: 180° horizontal, 120° vertical
- focal length: 2.8mm (wide-angle)
- low-light performance: capable of operating in various lighting conditions

### lidar

- type: high-precision lidar sensor
- range: up to 5 meters
- accuracy: ±2 cm
- field of view: 360° horizontal, 90° vertical
- integration: seamlessly integrates with the existing gesture recognition system for enhanced depth perception and accuracy


### processor

- onboard processor: custom-designed image processing chip
- ram: 1gb lpddr4 for fast data processing
- storage: 4gb emmc for firmware and configuration data

### ports

- interface: usb-c 3.1 gen 2 (10 gbps)
- cable: 1m usb-c cable included
- compatibility: macos 10.15+, windows 10+

### power

- power source: usb-c (bus-powered)
- power consumption: 2.5w typical, 4w max

### environment

- operating temperature: 0°c to 40°c (32°f to 104°f)
- storage temperature: -20°c to 60°c (-4°f to 140°f)
- humidity: 10% to 90% non-condensing

### software

- firmware: field-upgradable via handy app

### extras

- mounting: non-slip base with twist-lock system for easy attachment/detachment

### contents

- 1x hemi device
- 1x 1m usb-c cable
- quick start guide
- access code for handy software download

### setup

(detailed unboxing instructions, positioning guidelines, and connection instructions would be provided here)

### care

- clean the device regularly with a soft, dry cloth
- avoid exposing the device to extreme temperatures or humidity
- store in a cool, dry place when not in use

### issues

(common hardware issues and their solutions would be listed here)

## support

(this section would include common issues and solutions, instructions for reporting bugs, contact information for support, and community forum guidelines)

## performance

(hardware placement strategies, software configuration tips, and gesture design for speed would be detailed here)

## security

since the device captures images of the user's environment, addressing potential security and privacy concerns is essential. the data transmitted between the device and the computer is encrypted, and privacy settings allow users to control what information is shared.

## releases

(would include version history, changelog, known issues, and the product roadmap)

## community

(information on contributing to handy, showcases of community projects, educational resources, and the handy blog would be provided here)

### presets

(information on accessing, rating, and sharing community presets would be detailed here)

### guidelines

(code of conduct, submission and review process, and licensing information would be detailed here)