import streamlit as st
import random
import string
import json

def app():
    st.title("Classroom Home Page")

    def get_user_data_file(user_id):
        return f"user_data_{user_id}.json"

    def load_user_data(user_id):
        user_data_file = get_user_data_file(user_id)
        try:
            with open(user_data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"joined_classes": []}

    def save_user_data(user_id, user_data):
        user_data_file = get_user_data_file(user_id)
        with open(user_data_file, "w") as file:
            json.dump(user_data, file)

    def generate_random_code():
        code_length = 6
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(code_length))

    def render_classroom_page(classroom_data_file, classroom_code):
        try:
            with open(classroom_data_file, "r") as file:
                classroom_data = json.load(file)

            # Update Streamlit page title
            st.title(f"Classroom: {classroom_data['subject']}")
            
            # Show only relevant information
            st.subheader("Classroom Posts")

            # Show existing posts
            for post in classroom_data["posts"]:
                st.write(post)

            # Allow the user to post new messages
            new_post = st.text_area("Post your message:")
            if st.button("Post"):
                classroom_data["posts"].append(new_post)
                with open(classroom_data_file, "w") as file:
                    json.dump(classroom_data, file)
                st.success("Message posted successfully!")

        except FileNotFoundError:
            st.warning(f"Classroom data not found for code: {classroom_code}")

    user_id = st.session_state.user_id

    if user_id:
        user_data = load_user_data(user_id)
        user_classrooms = user_data.get("joined_classes", [])

        if user_classrooms:
            st.write("Your Classrooms:")
            for classroom_code in user_classrooms:
                classroom_data_file = f"classroom_data_{classroom_code}.json"
                try:
                    with open(classroom_data_file, "r") as file:
                        classroom_data = json.load(file)
                    st.write(f"Classroom Code: {classroom_code}")
                    st.write(f"Subject: {classroom_data.get('subject', 'Unknown')}")
                    
                    # Check if "Go to [classroom_name]" button is clicked
                    if st.button(f"Go to {classroom_data['subject']}", key=f"go_to_{classroom_code}"):
                        # Render the classroom page
                        render_classroom_page(classroom_data_file, classroom_code)
                        break  # Break the loop to prevent further rendering
                except FileNotFoundError:
                    st.warning(f"Classroom data not found for code: {classroom_code}")

        if not st.session_state.get("classroom_page_rendered", False):
            new_classroom_name = st.text_input("Enter the name of the new classroom:")
            if st.button("Create Classroom") and new_classroom_name:
                code = generate_random_code()
                classroom_data = {"id": len(user_classrooms) + 1, "subject": new_classroom_name, "posts": [], "owner": user_id}
                classroom_data_file = f"classroom_data_{code}.json"
                with open(classroom_data_file, "w") as file:
                    json.dump(classroom_data, file)
                user_data.setdefault("joined_classes", []).append(code)
                save_user_data(user_id, user_data)
                st.success(f"Classroom '{new_classroom_name}' created successfully!")
        else:
            st.session_state.classroom_page_rendered = False  # Reset the flag

    else:
        st.warning("You need to log in to view your classrooms.")

# Placeholder function for main (you can fill in the details)
def main():
    app()

if __name__ == "__main__":
    main()
