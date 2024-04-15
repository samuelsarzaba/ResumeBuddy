import Nav from "@/components/Nav";
import { Button } from "@/components/ui/button";
import Image from "next/image";

export default function Home() {
  return (
    <main className="flex p-24">
      <Nav />
      <section className="py-24 flex flex-col gap-8">
        <h1>Penis</h1>
        <div className="flex gap-6 py-6"></div>
      </section>
      <div>
        <Button>Learn More</Button>
      </div>
    </main>
  );
}
