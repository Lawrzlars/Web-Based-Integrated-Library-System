import { NextResponse } from "next/server"
import { loadPatrons, addPatron, updatePatron, deletePatron } from "@/lib/library-data"

export async function GET() {
  const patrons = await loadPatrons()
  return NextResponse.json(patrons)
}

export async function POST(request: Request) {
  const body = await request.json()
  const { name } = body
  
  if (!name) {
    return NextResponse.json({ success: false, message: "Name is required." }, { status: 400 })
  }
  
  const result = await addPatron(name)
  return NextResponse.json(result, { status: result.success ? 201 : 400 })
}

export async function PUT(request: Request) {
  const body = await request.json()
  const { id, name } = body
  
  if (!id || !name) {
    return NextResponse.json({ success: false, message: "ID and name are required." }, { status: 400 })
  }
  
  const result = await updatePatron(Number(id), name)
  return NextResponse.json(result, { status: result.success ? 200 : 404 })
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get("id")
  
  if (!id) {
    return NextResponse.json({ success: false, message: "Patron ID is required." }, { status: 400 })
  }
  
  const result = await deletePatron(Number(id))
  return NextResponse.json(result, { status: result.success ? 200 : 400 })
}
