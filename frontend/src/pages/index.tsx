import TeacherAccountForm from "@/components/teacheraccountform";

export default function Home() {
  return (
    <div
      className={`grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]`}
    >
    <b>Welcome to Darwin</b>

      <p>If you are a teacher. Please submit a request to make an account</p>
      <TeacherAccountForm/>

      <p>If you already have an account: </p>
      <button>Login</button>
    </div>
  );
}
