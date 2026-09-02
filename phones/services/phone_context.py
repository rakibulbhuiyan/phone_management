class PhoneContextBuilder:

    def build(self, phones):
        contexts = []

        for phone in phones:
            context = f"""
Phone Name: {phone.name}

Display:
- Size: {phone.display_size}
- Type: {phone.display_type}

Performance:
- Processor: {phone.processor}
- RAM: {phone.ram}
- Storage: {phone.storage}

Camera:
- Main Camera: {phone.main_camera}
- Selfie Camera: {phone.selfie_camera}

Battery:
- Battery: {phone.battery}

Operating System:
- OS: {phone.operating_system}

Source:
- {phone.source_url}
"""

            contexts.append(context.strip())

        return "\n\n---\n\n".join(contexts)