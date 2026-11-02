# ResQMesh-Smart-Disaster-Rescue-and-Coordination-System
It is a communication technique when an unexpected disaster was carried out !
Communication is the only medium which can act as a bridge between rescue operator and the victim. What is the communication has been become a Disaster!!

To solve this issue, we just implemented a plan which can help to manage and resolve this serious issue. For this a pragmatic approach is required. So we developed a communication system "mobile with walkie talkie communication".
I just seem funny right? but we just came that live. The project is now at initial phase. When builds a communication network which will be only active during disaster.

Understanding the Complete System

ResQMesh is designed around three important entities:

Mobile users: People in disaster-affected areas who need to communicate or request assistance.

Elevated communication relay: A proposed floating communication unit, such as a tethered balloon or aerostat carrying suitable communication equipment.

Ground control station: A server and emergency coordination system that receives information and connects it to rescue operators.

The floating relay is intended to improve communication coverage by placing communication equipment above ground-level obstacles. It acts as a communication bridge between affected regions and the ground infrastructure.

flowchart TD
    A[Person in Disaster-Affected Area]
    B[ResQMesh Mobile Interface]
    C[Local Communication Gateway]
    D[Floating Relay Unit]
    E[RF Communication Link]
    F[Ground Receiver / Gateway]
    G[Python Backend Server]
    H[Emergency Control Dashboard]
    I[Rescue Operator]
    J[Rescue Team]

    A --> B
    B --> C
    C <-->|Wireless Communication| D
    D <-->|RF Communication| F
    F <--> G
    G <--> H
    H <--> I
    I --> J

    How the proposed communication works

A person opens the ResQMesh mobile interface and sends a voice message or emergency request.

The mobile device connects to a nearby communication gateway.

The gateway forwards the information to the floating relay through a suitable wireless connection.

The floating unit uses its communication equipment to relay the information through an RF link to another receiving station.

The receiving station forwards the recovered information to the ground server.

The backend processes the information and makes it available to authorized rescue operators.

Rescue operators can respond and coordinate assistance.

The reverse communication path can also be used to deliver messages from rescue operators back to affected people.

The exact hardware, wireless access method, radio frequency, and communication protocol will be finalized during the next development stages.

3. Why a Floating Communication Relay?

One of the major challenges in disaster communication is the loss of reliable network infrastructure.

Buildings, hills, damaged roads, and other obstacles can affect ground-level wireless communication.

Our proposed solution explores the use of an elevated communication relay.

A tethered balloon or aerostat could carry suitable antennas and radio equipment above ground-level obstacles.

Proposed advantages

Improved line-of-sight communication in suitable terrain.

An elevated point for relaying communication.

Potential communication support for isolated areas.

A deployable communication infrastructure for emergency operations.

The actual coverage will depend on antenna height, radio frequency, transmit power, antenna characteristics, terrain, interference, and other engineering factors.

The floating relay is currently a design concept and requires hardware development, safety evaluation, and practical testing.

4. What We Have Built So Far

We did not want to limit this project to an idea or a theoretical communication diagram. Therefore, we started by building a software prototype to understand how voice information can be transmitted, processed, and recovered.

Our initial implementation focuses on a mobile-to-server voice communication system.

Current prototype components

A browser-based voice recording interface.

A Python server that receives audio from a client.

Local network communication between devices.

WAV audio processing.

Software-based BPSK modulation and demodulation.

A simulated communication channel.

Audio reconstruction at the receiving side.

The current prototype provides a foundation for understanding the communication and signal-processing stages required for the larger ResQMesh system.

Current prototype architecture

flowchart TD
    A[Mobile Phone / Browser]
    B[Voice Recording]
    C[Audio Data]
    D[Local Wi-Fi Network]
    E[Python Server]
    F[Audio Processing]
    G[BPSK Software Simulation]
    H[Demodulation and Recovery]
    I[Recovered Audio]
    J[Receiver Interface]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J

Current implementation: The mobile browser sends recorded audio over a local Wi-Fi network to the Python server. The server processes the audio through a software BPSK simulation and reconstructs the recovered audio for the receiver interface.

This is not yet a physical radio communication system.

5. How Data Travels Between the Mobile and Python Server

Understanding the data flow is important to understanding our current prototype.

Step 1 – Voice capture

The user records a voice message through the mobile browser.

The browser uses its microphone access functionality to capture audio.

Step 2 – Audio conversion

The recorded voice is processed into a WAV audio file.

Our prototype uses audio configured around:

Sample rate: 16,000 Hz.

Channels: Mono.

Sample format: 16-bit audio.

Step 3 – Wireless data transfer

The mobile browser sends the recorded audio to the Python server using an HTTP request over the local network.

Both devices must be connected to a reachable network.

Step 4 – Server-side processing

The Python server receives the audio and processes it using Python libraries such as NumPy and SciPy.

Step 5 – BPSK simulation

The audio samples are represented as binary data.

The software simulation then performs:

Binary data conversion.

BPSK symbol mapping.

Simulated channel transmission.

Addition of simulated noise.

Demodulation.

Bit recovery.

BPSK represents binary values using two carrier phase states separated by 180 degrees.

Step 6 – Audio reconstruction

The recovered binary data is converted back into audio samples and reconstructed as a WAV file.

Step 7 – Receiving the audio

The receiver interface requests the processed audio from the Python server and plays it back.

This demonstrates the software-based signal-processing workflow.

Important technical distinction: The current network transfer uses local Wi-Fi. BPSK is simulated in software after the server receives the audio. No actual RF signal is currently transmitted through an antenna.

6. How the Current Prototype Connects to the Future Floating Relay

The existing prototype helps us develop and understand the software side of communication.

The next major engineering challenge is replacing the local-network communication link with a suitable radio communication link.

The planned evolution is:

CURRENT PROTOTYPE

Mobile Browser
      |
      | Local Wi-Fi
      |
Python Server
      |
Software BPSK Simulation
      |
Recovered Audio


FUTURE PROPOSED SYSTEM

Mobile Interface
      |
Communication Gateway
      |
Floating Relay Unit
      |
Physical RF Transmission
      |
Ground Receiving Station
      |
Backend Server
      |
Emergency Control Dashboard
      |
Rescue Operator

The future system will require suitable radio hardware, antennas, a compatible communication protocol, and testing in a legally permitted frequency band.

The mobile device will not automatically communicate with an SDR just because BPSK is implemented in software. A compatible radio gateway or radio interface will be needed to connect the mobile application to the RF communication system.

7. Other Planned Modules

ResQMesh is not limited to voice communication. We are also planning additional features to support disaster management.

SOS and Rescue Coordination

A citizen should be able to submit an SOS request containing emergency details and available location information.

The control-room dashboard will allow authorized operators to review incidents, assign rescue teams, track progress, and confirm safety.

Weather Intelligence

Weather information such as rainfall, temperature, humidity, wind speed, precipitation probability, and weather warnings can help authorities understand conditions in affected regions.

Ultra Battery Saver

An emergency-focused mobile interface will provide quick access to essential applications and battery-saving settings when charging facilities are unavailable.

These modules are planned extensions and will be developed and integrated progressively.

8. Technology Stack

Component

Technology

Mobile interface

HTML, CSS, JavaScript

Backend server

Python

Audio recording

Browser MediaRecorder

Audio processing

NumPy, SciPy

Audio format

WAV

Current networking

Local Wi-Fi / HTTP(S)

Digital modulation

BPSK software simulation

Future radio communication

SDR hardware

Future signal-processing environment

GNU Radio

Proposed dashboard

React

Proposed database

PostgreSQL / Firebase

Proposed weather integration

Weather API

Proposed Android module

Kotlin / Android Studio

9. Current Development Status

Feature

Development status

Browser-based voice recording

Implemented in prototype

Python voice server

Implemented in prototype

Local Wi-Fi audio transfer

Demonstrated

WAV audio processing

Implemented in prototype

BPSK software simulation

Demonstrated

Simulated channel and noise

Demonstrated

Audio demodulation and reconstruction

Demonstrated

Floating communication relay

Proposed

Physical SDR transmission

Not implemented

Antenna-based RF communication

Not implemented

SOS and rescue dashboard

Planned

Weather intelligence

Planned

Ultra Battery Saver

Planned

10. What Needs to Be Developed Next?

Our next development stages will focus on making the concept functional beyond the software simulation.

Improve the current voice communication prototype.

Implement reliable sender-to-receiver message delivery.

Design a communication gateway between mobile devices and radio equipment.

Select suitable SDR transmitter and receiver hardware.

Develop a physical BPSK transmission and reception pipeline.

Design and test suitable antennas.

Develop the floating relay communication unit.

Establish communication between the relay and ground station.

Build the SOS reporting and emergency dashboard.

Integrate weather information.

Develop the Android emergency interface.

Perform controlled end-to-end testing.

11. Our Vision

Our goal is to explore a communication system that can be deployed when conventional communication infrastructure becomes unreliable.

ResQMesh is an attempt to rethink emergency communication by combining mobile technology, digital signal processing, radio communication, elevated relay infrastructure, and disaster-response coordination.

We are starting with a software prototype, learning and validating each communication stage, and progressively working towards a system that can support real-world disaster-response operations.

Because during a disaster, communication should never become another obstacle to rescue.

