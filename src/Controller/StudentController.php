<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;




final class StudentController extends AbstractController
{
    #[Route('/getall', name: 'app_student')]
    public function index(): Response
    {
        $moyenne =20;
        $students= ["ons","aziz","sarra","med"];

        return $this->render('student/index.html.twig', [
            'students' => $students, 
            'moy2' => $moyenne,
            

        ]);
    }
 #[Route('/add', name: 'addS')]
  public function addStudent(): Response
    {
        return new Response("Added successsffuuullyyyyyyy!!!!!!");
    }
#[Route('/get/infoStudent', name: 'getI')]
  public function getStudent(): Response
    {
        return new Response("3A213!!!!!!");
    }
#[Route('/get/{name}', name: 'getS')]
  public function getStudentByName($name): Response
    {
        return new Response("Added successsffuuullyyyyyyy!!!!!!".$name);
    }





}
