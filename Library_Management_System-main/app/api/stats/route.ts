import { NextResponse } from "next/server"
import { getStatistics } from "@/lib/library-data"

export async function GET() {
  const stats = await getStatistics()
  return NextResponse.json(stats)
}
