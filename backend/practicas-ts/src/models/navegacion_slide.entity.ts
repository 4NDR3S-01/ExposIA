import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('navegacion_slides')

export class NavegacionSlide {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    grabacion_id: number;

    @Column()
    slide_id: number;

    @Column()
    timestamp: number;

    @Column({nullable: true })
    tipo_navegacion: string; // 'siguiente', 'anterior', 'inicio', 'fin', etc.\
}