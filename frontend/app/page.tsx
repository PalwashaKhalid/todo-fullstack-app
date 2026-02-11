export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Todo App</h1>
        <p className="text-lg text-gray-600 mb-8">Manage your tasks efficiently</p>
        <div className="space-x-4">
          <a
            href="/login"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Sign in
          </a>
          <a
            href="/signup"
            className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}
