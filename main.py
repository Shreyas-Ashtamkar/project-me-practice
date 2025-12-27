import datetime
from email_me_anything import select_random_row, build_html_content, send_email

if __name__ == "__main__":
    data = select_random_row(
        csv_path="500ProjectsList.csv",
        skip_header=True
    )
    
    data.update({
        "sender_name": "Shreyas from Laptop",
        "recipient_name": "Shreyas",
        "current_week": 1,
        "tags": f"{(data['Domain']+' Domain')}{' · Group ' + data['Group'] if data['Group'] else ''}{' · Step ' + data['Step'] if data['Step'] else ''} · {data['Weeks']} {'Weeks' if data['Weeks']!='1' else 'Week'}"
    })
    
    html_content = build_html_content(
        template_path="email-template.html",
        data=data,
        variable_map={
            "id": "ID",
            "name": "Project Idea",
            "description": "Description",
            "tags": "tags",
            "recipient_name": "recipient_name",
            "current_week": "current_week",
            "sender_name": "sender_name"
        }
    )
    
    status = send_email(
        subject = datetime.datetime.now().strftime("%B %d, %Y"),
        html_content = html_content,
        sender={"email": "laptop.shreyas@dev-master.in", "name": "Shreyas from Laptop"},
        recipients=[{"email": "shreyas.ashtamkar18@gmail.com", "name": "Shreyas"}]
    )
    
    print(f"Email send status: {status}")