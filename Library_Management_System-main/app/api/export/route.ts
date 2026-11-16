import { NextResponse } from "next/server"
import { exportBooksToCSV, exportPatronsToCSV } from "@/lib/library-data"

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const type = searchParams.get("type")
  
  if (type === "books") {
    const csv = await exportBooksToCSV()
    return new NextResponse(csv, {
      headers: {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=books.csv",
      },
    })
  } else if (type === "patrons") {
    const csv = await exportPatronsToCSV()
    return new NextResponse(csv, {
      headers: {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=patrons.csv",
      },
    })
  }
  
  return NextResponse.json({ error: "Invalid type. Use 'books' or 'patrons'." }, { status: 400 })
}
