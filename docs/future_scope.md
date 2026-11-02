
# ResQMesh – Future Scope and Development Roadmap

## 1. Introduction

ResQMesh aims to evolve from a basic software communication prototype into a dedicated communication network designed for emergency situations.

The current implementation demonstrates voice-message communication between a mobile phone and a laptop through a Python server over a common Wi-Fi network.

The future objective is to establish communication between multiple devices using dedicated radio communication hardware, reducing dependence on conventional cellular infrastructure.

---

## 2. Dedicated Communication Network

The primary goal is to develop a communication network that allows multiple devices to exchange voice and emergency information, similar to walkie-talkies.

### Planned Capabilities

- Communication between multiple devices.
- Two-way voice communication.
- Dedicated communication channels.
- Device identification.
- Emergency message transmission.
- Communication without conventional cellular networks.
- Reliable message delivery and acknowledgement.

A suitable communication protocol will be required to coordinate multiple users and prevent transmission conflicts.

---

## 3. SDR-Based Radio Communication

Software-Defined Radio (SDR) is one of the core technologies planned for the physical communication system.

SDR allows several radio signal-processing functions to be implemented or configured through software.

### Planned SDR Implementation

**Transmitter:**

1. Capture voice through a microphone.
2. Convert the analog audio signal into digital samples.
3. Encode the digital information into binary data.
4. Apply digital modulation using SDR.
5. Generate the corresponding RF signal.
6. Transmit the signal through an antenna.

**Receiver:**

1. Capture the incoming RF signal through an antenna.
2. Process the received signal using an RF front end.
3. Demodulate the signal using SDR.
4. Recover the transmitted digital information.
5. Decode the audio data.
6. Play the recovered voice through a speaker.

### Digital Modulation

BPSK (Binary Phase Shift Keying) is one of the modulation techniques explored in the project.

It represents binary information using two carrier phases separated by 180 degrees.

Further experiments will evaluate suitable modulation techniques, signal quality, communication range, and reliability.

---

## 4. Floating Communication Module

Another proposed component is a compact water-based floating communication module.

The concept is an inflatable floating structure similar to a swimming tube, equipped with a central waterproof electronics enclosure and an approximately 3-metre antenna mast.

### Proposed Components

- Inflatable floating body.
- Waterproof electronics enclosure.
- SDR transmitter and receiver equipment.
- RF antenna and supporting mast.
- Rechargeable battery.
- Power management system.
- Anchoring and stabilization mechanism.

### Intended Purpose

The floating module is intended to act as an intermediate communication relay between affected regions and a ground receiving station.

Its deployment will depend on the availability of suitable water bodies and environmental conditions.

---

## 5. Ground Receiving Station

A ground receiving station is proposed to receive and process information transmitted through the radio communication system.

### Planned Functions

- Receive RF transmissions.
- Recover digital information.
- Forward messages to a local backend server.
- Store emergency communication records.
- Provide information to authorized rescue operators.

A locally hosted backend could allow essential coordination to continue even when internet connectivity is unavailable.

---

## 6. SOS and Rescue Coordination

ResQMesh also aims to support disaster-response operations through an emergency coordination system.

### Planned Features

- Emergency SOS submission.
- Location sharing when available and authorized.
- Unique incident identification.
- Emergency priority classification.
- Rescue team assignment.
- Incident status tracking.
- Safety confirmation.

---

## 7. Weather Intelligence

Weather information could help rescue operators make better-informed decisions.

### Planned Information

- Temperature.
- Humidity.
- Rainfall.
- Precipitation probability.
- Wind speed and direction.
- Weather warnings.

The system may integrate external weather APIs to provide updated weather information.

---

## 8. Ultra Battery Saver

An emergency-focused mobile interface is also planned.

Its objective is to help users preserve battery power during emergencies while keeping essential communication features accessible.

Potential features include:

- Minimal emergency interface.
- Quick access to communication features.
- Dark interface.
- Battery-saving recommendations.
- Access to supported Android battery settings.

Actual control over system-wide battery usage will depend on Android permissions and device capabilities.

---

## 9. Development Roadmap

The proposed development will follow these stages:

### Phase 1 – Software Prototype
- Develop the Python communication server.
- Establish mobile-to-laptop communication over Wi-Fi.
- Implement voice recording and message transfer.
- Test the communication workflow.

### Phase 2 – Communication Protocol
- Support multiple devices.
- Implement device identification.
- Introduce message acknowledgement.
- Add error detection and retransmission.
- Improve communication reliability.

### Phase 3 – SDR Integration
- Select suitable SDR hardware.
- Develop transmitter and receiver workflows.
- Experiment with digital modulation.
- Test physical RF communication using permitted frequencies.

### Phase 4 – Floating Module Development
- Design the inflatable floating structure.
- Develop the waterproof electronics enclosure.
- Integrate the antenna and SDR equipment.
- Implement power management and anchoring.
- Conduct controlled stability and safety tests.

### Phase 5 – Disaster Coordination
- Develop the local backend.
- Build the emergency dashboard.
- Implement SOS and rescue coordination.
- Explore weather information integration.

### Phase 6 – Testing and Evaluation
- Measure communication range.
- Evaluate signal quality.
- Measure packet loss and bit error rate.
- Test multi-device communication.
- Evaluate performance under controlled environmental conditions.

---

## 10. Long-Term Vision

The long-term goal of ResQMesh is to explore an alternative communication infrastructure that can support emergency communication when conventional networks become unavailable.

By combining software-based communication, SDR technology, RF communication, and floating relay infrastructure, we aim to develop a system that can support information exchange and rescue coordination during disasters.

**Connecting Information. Coordinating Rescue. Confirming Safety.**

---

## Development Disclaimer

The dedicated radio network, SDR hardware integration, floating communication module, SOS platform, and other modules described in this document are proposed future developments.

They are not currently operational features of the software prototype. Physical radio implementation will require hardware integration, regulatory compliance, safety evaluation, and real-world testing.
