
export default function TeacherAccountForm() {
    return (
        <div>
            <form action="/account" method="POST">
                <label htmlFor="firstname">First Name: </label>
                <input type="text" name="firstname" id="firstname" />
                <label htmlFor="lastname">Last Name: </label>
                <input type="text" name="lastname" id="lastname" />
                <label htmlFor="email">Email: </label>
                <input type="email" name="email" id="email" />
                <input type="submit" value="submit"/>
            </form>
        </div>
     );
}