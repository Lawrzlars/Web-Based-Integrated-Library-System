import { NextResponse } from "next/server"
import { loadBooks, addBook, updateBook, deleteBook } from "@/lib/library-data"

export async function GET() {
  const books = await loadBooks()
  return NextResponse.json(books)
}

export async function POST(request: Request) {
  const body = await request.json()
  const { title, author, year } = body
  
  if (!title || !author || !year) {
    return NextResponse.json({ success: false, message: "Title, author, and year are required." }, { status: 400 })
  }
  
      // Block only if ANOTHER book has the same title AND the same author
  if (title?.trim() && author?.trim()) {
    const normalize = (value: string) =>
      value.trim().replace(/\s+/g, " ").toLowerCase()

    const books = await loadBooks()
    const duplicate = books.find(
      (book) =>
        normalize(book.title) === normalize(title) &&
        normalize(book.author) === normalize(author)
    )

    if (duplicate) {
      return NextResponse.json(
        { success: false, message: "This book already exists in your library!" },
        { status: 409 }
      )
    }
  }

  const result = await addBook(title, author, Number(year))
  return NextResponse.json(result, { status: result.success ? 201 : 400 })
}

export async function PUT(request: Request) {
  const body = await request.json()
  const { id, title, author, year } = body
  
  if (!id) {
    return NextResponse.json({ success: false, message: "Book ID is required." }, { status: 400 })
  }

    // Block only if ANOTHER book has the same title AND the same author
  if (title?.trim() && author?.trim()) {
    const normalize = (value: string) =>
      value.trim().replace(/\s+/g, " ").toLowerCase()

    const books = await loadBooks()
    const duplicate = books.find(
      (book) =>
        book.id !== Number(id) &&
        normalize(book.title) === normalize(title) &&
        normalize(book.author) === normalize(author)
    )

    if (duplicate) {
      return NextResponse.json(
        { success: false, message: "This book already exists in your library!" },
        { status: 409 }
      )
    }
  }
  
  const result = await updateBook(Number(id), { title, author, year: year ? Number(year) : undefined })
  return NextResponse.json(result, { status: result.success ? 200 : 404 })
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get("id")
  
  if (!id) {
    return NextResponse.json({ success: false, message: "Book ID is required." }, { status: 400 })
  }
  
  const result = await deleteBook(Number(id))
  return NextResponse.json(result, { status: result.success ? 200 : 400 })
}

