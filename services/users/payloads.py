from faker import Faker

fake = Faker()


class Payloads:

    def update_me(self, display_name: str, bio: str, is_private:bool):
        return {"display_name": display_name,
                "bio": bio,
                "is_private": is_private
                }

    def update_avatar(self, file_path: str):
        return {
            "file": f"{file_path}"
        }