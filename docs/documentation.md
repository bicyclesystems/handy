# handy

## Introduction

handy is a revolutionary tool that turns your everyday spaces into an intuitive, ergonomic platform for interacting seamlessly with your computer. instead of relying on a traditional desktop mouse or trackpad, it leverages advanced technology to convert your hand gestures into digital commands, redefining the way you engage with your digital world.

handy was developed with the vision of making computers more accessible, intuitive, and enjoyable. it aims to provide a more natural and ergonomic alternative to traditional input devices.

### Core features and benefits

- Advanced gesture recognition technology
- Adaptable to different surfaces
- open-source api for customization and integration
- versatile for various user needs, from casual browsing to professional applications

### Target audience

handy is designed for creative people such as:

- designers
- musicians
- casual users and anyone looking for a more natural and ergonomic alternative to the traditional mouse

### System overview

handy's system consists of hardware and software components working together to capture hand movements and translate them into digital commands. the core of this system is the advanced algorithms that adapt to different surfaces for consistent performance.

### handy app

the handy app provides a simple, intuitive user interface to configure settings. it includes:

- Management of gesture presets
- Device firmware updates
- Status bar indicator for motion capturing states
- gesture customization tools

Supported platforms: macOS and Windows

### handy framework

The handy framework is an open-source platform that allows users to:

- Create, customize, and share gestures
- Contribute to the development of new gestures
- Expand the range of supported gestures
- Improve the overall user experience through community collaboration

### hemi

hemi is a small, hemisphere-shaped device that captures movement with high performance and ergonomics. It enhances the user experience, elevating gesture control technology from casual to professional needs.

Key features:

- Compact, high-resolution camera with a wide field of view
- Infrared or depth-sensing capabilities for better performance and adaptability
- Sleek, modern design that blends well with various desk setups

## handy app

### System Requirements

(Specific hardware requirements, software dependencies, and OS compatibility would be listed here)

### Installation

- Download the handy application installer for your operating system (macOS or Windows).
- Run the installer and follow the on-screen instructions.
- Once installed, launch the handy application.

### Initial Configuration

- Open the handy application.
- Follow the on-screen calibration process.
- Adjust sensitivity settings to your preference.
- Choose a default gesture preset or create a custom one.
    
    (Information on available preset categories and how to activate/switch presets would be provided here)
    

### Using pre-defined gesture sets

handy includes a virtual trackpad driver that interfaces with the operating system's trackpad APIs. This driver is responsible for passing the translated gesture events to the operating system. It implements a mechanism to map the recognized gestures into trackpad events, such as taps, swipes, and pinches, compatible with the trackpad APIs of macOS and Windows.

| Gesture Name | Description |
| --- | --- |
| Move ✅ | Finger touch and moves. |
| Single Tap ✅ | A quick tap with one finger on the table surface, equivalent to a left-click on a traditional mouse. |
| Double Tap ✅ | Two quick taps with one finger on the table surface, used to open files or applications, and access context menus. |
| Two-Finger Tap ✅ | A simultaneous tap with two fingers on the table surface, equivalent to a right-click on a traditional mouse. |
| Tap and Hold ✅ | Tapping and holding one finger on the table surface, equivalent to clicking and holding the left mouse button. |
| Two-Finger Scroll ✅ | Placing two fingers on the table surface and moving them up or down to scroll vertically or left and right to scroll horizontally. |
| Pinch-to-Zoom ✅ | Placing two fingers on the table surface and moving them closer together or further apart to zoom in or out of content. |
| Rotate ✅ | Placing two fingers on the table surface and moving them in a circular motion to rotate objects or content. |
| Three-Finger Swipe ✅ | Swiping three fingers across the table surface to switch between applications, desktops, or browser tabs. |
| Four-Finger Swipe ✅ | Swiping four fingers across the table surface to show the desktop or reveal all open windows (similar to Exposé or Task View on macOS and Windows). |
| Keyboard Events |  |

### User interface guide

(Detailed description of the app's dashboard, menu structure, and customization options would be provided here)

### Basic operations

- Starting/stopping gesture recognition
- Switching between gesture sets
- Viewing active gestures

### Settings and configurations

The handy app includes options for:

- Sensitivity adjustments
- Gesture customization
- Managing gesture presets
- Updating device firmware
- Integration with other software

### calibration process

(Step-by-step calibration guide and information on when to recalibrate would be included here)

### Updating the software

(Instructions for checking for updates, the update process, and rollback procedures would be detailed here)

### Status bar indicator

The handy app includes a small desktop indicator application that displays the current status of the motion capturing:

- Active
- Error
- Processing/Input
- Standby

This indicator replaces the need for a physical LED indicator on the device itself. handy automatically looks for active software that works with its active gestures. If it finds any, it connects the gestures to that software.

## handy framework

### sensor technology

- Gesture Recognition: Advanced computer vision algorithms
- Motion Tracking: 6-axis motion tracking (accelerometer + gyroscope)
- Surface Adaptation: AI-driven surface recognition for consistent performance

### Creating custom gestures

(Instructions for the gesture recording process, defining gesture parameters, and testing/refining gestures would be provided here)

### Best practices for reliable detection

(Tips for optimal lighting, hand positioning, and gesture complexity would be detailed here)

### Troubleshooting recognition issues

(Common recognition errors, calibration tips, and guidelines for when to retrain gestures would be listed here)

### Creating and editing Gestures Presets

(Information on authoring tools and the validation process for gesture presets would be provided here)

(Workflow for creating presets, adding/removing gestures, and setting default presets would be detailed here)

### gestures.handy Framework

The gestures.handy file uses a JSON format. Here's an example structure:

```json
{
  "meta": {
    "version": "1.0",
    "name": "Trackpad Gesture Set"
  },
  "models": {
    "handRecognition": "default_model",
    "additionalModels": []
  },
  "gestures": {
    "primitive": [
      {
        "name": "Tap",
        "code": "function tap() { /* code here */ }"
      },
      {
        "name": "Scroll",
        "code": "function scroll() { /* code here */ }"
      }
      // more primitive gestures
    ],
    "custom": [
      {
        "name": "TwoFingerTap",
        "code": "function twoFingerTap() { /* code here */ }"
      }
      // more custom gestures
    ]
  },
  "mapping": null // No need for mapping here as it's handled by the SDK on the software side
}
```

### Mapping gestures to system actions

(Available system actions and instructions for creating basic mappings would be listed here)

### Creating custom mappings

(Guidelines for defining custom actions and using macros/scripts would be provided here)

### Context-sensitive gestures

(Instructions for setting up application-specific gestures and using gestures based on system state would be detailed here)

### Advanced mapping techniques

(Information on chaining multiple actions, using modifiers with gestures, and creating adaptive gesture responses would be provided here)

### Version control and compatibility

(Details on the versioning scheme and backward compatibility considerations would be included here)

## hemi

hemi, the sensor that powers handy, captures the magic of your gestures. this sleek, half-dome device acts as handy's eyes, sending ultra-wide 180-degree black-and-white images at lightning speed. with its keen vision, hemi enables handy to interpret your movements into computer commands with instantaneous responsiveness, bringing your gestures to life on screen.

the device has a half-spherical shape with a flat base, allowing it to sit stably on the table surface. this design provides an elegant, modern appearance while ensuring a wide field of view for capturing gestures.

### physical characteristics

- Dimensions:
    - Height: 2.5 cm
    - Width: 5 cm
    - Depth: 5 cm
- Weight: 100 grams (estimated, to be confirmed)
- Design: Half-spherical shape with a flat base
- Materials: High-quality plastic and metal for durability and heat dissipation

### camera

- Type: High-resolution depth-sensing camera
- Resolution: 1080p (1920x1080 pixels)
- Frame Rate: 120 fps for ultra-smooth motion capture
- Field of View: 180° horizontal, 120° vertical
- Focal Length: 2.8mm (wide-angle)
- Low-light Performance: Capable of operating in various lighting conditions

### processing

- Onboard Processor: Custom-designed image processing chip
- RAM: 1GB LPDDR4 for fast data processing
- Storage: 4GB eMMC for firmware and configuration data

### connectivity

- Interface: USB-C 3.1 Gen 2 (10 Gbps)
- Cable: 1m USB-C cable included
- Compatibility: macOS 10.15+, Windows 10+

### power

- Power Source: USB-C (bus-powered)
- Power Consumption: 2.5W typical, 4W max

### environmental specifications

- Operating Temperature: 0°C to 40°C (32°F to 104°F)
- Storage Temperature: -20°C to 60°C (-4°F to 140°F)
- Humidity: 10% to 90% non-condensing

### Software Integration

- Firmware: Field-upgradable via handy app

### additional features

- Mounting: Non-slip base with twist-lock system for easy attachment/detachment

### package contents

- 1x hemi device
- 1x 1m USB-C cable
- Quick start guide
- Access code for handy software download

### setup and installation

(Detailed unboxing instructions, positioning guidelines, and connection instructions would be provided here)

### maintenance and care

- Clean the device regularly with a soft, dry cloth
- Avoid exposing the device to extreme temperatures or humidity
- Store in a cool, dry place when not in use

### troubleshooting

(Common hardware issues and their solutions would be listed here)

## troubleshooting and support

(This section would include common issues and solutions, instructions for reporting bugs, contact information for support, and community forum guidelines)

## Performance

(Hardware placement strategies, software configuration tips, and gesture design for speed would be detailed here)

## security

Since the device captures images of the user's environment, addressing potential security and privacy concerns is essential. The data transmitted between the device and the computer is encrypted, and privacy settings allow users to control what information is shared.

## Release Notes

(would include version history, changelog, known issues, and the product roadmap)

## community and resources

(information on contributing to handy, showcases of community projects, educational resources, and the handy blog would be provided here)

### Community preset library

(Information on accessing, rating, and sharing community presets would be detailed here)

### community guidelines and contribution process

(Code of conduct, submission and review process, and licensing information would be detailed here)